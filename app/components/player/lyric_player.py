# coding : utf-8
import re
import sys
import time
import os
import threading

import inspect
import ctypes
import json
import base64

from PyQt5.QtMultimedia import QMediaPlayer
from common.kill_thread import stop_thread
from components.player.music_stream_queue import MusicStreamQueue
from common.lyric_format.krc_to_lrc import krc2lrc
LRC_PATH = 'resource\\Lyric\\'


class LrcPlayer(object):
    def __init__(self, player: QMediaPlayer, playlist: MusicStreamQueue, lyrics_window=False):
        self._init_lrc_content()

        self.lyrics_window = lyrics_window
        self.playlist = playlist
        self.player = player

        self.trans_mode = 0  # 翻译模式 0为不翻译 1为中文 2为罗马音
        self.is_pause = False

        self.thread_play_lrc = threading.Thread(target=self.__play_lrc_thread)

    def _init_lrc_content(self):
        self.information_dict = {}
        self.song_time_list = []  # 单位为毫秒
        self.trans_non_list = []
        self.trans_romaji_list = []
        self.trans_chinese_list = []
        self.len_song = 0

    def load_playlist(self, playlist: MusicStreamQueue) -> None:
        """
        Load playlist without affecting playback.

        :param playlist:
        :return: None
        """
        self.playlist = playlist
        self._reload_lrc_data()

    def _reload_lrc_data(self) -> None:
        """
        Make the in-class data correspond to the lyrics file data.

        :return: None
        """
        self.lrc_path = find_lrc_path(self.playlist.now_song_info["md5"])
        self.__load_lrc()
        self.len_song = len(self.song_time_list)
        if 'language' in self.information_dict.keys():
            self.__get_translation()

    def restart_thread(self) -> None:
        """
        Restart the thread that outputs the lyrics

        :return: None
        """
        self._reload_lrc_data()
        if self.thread_play_lrc.is_alive():
            stop_thread(self.thread_play_lrc)
        self.thread_play_lrc = threading.Thread(target=self.__play_lrc_thread)
        if not self.lrc_path:
            return
        self.thread_play_lrc.start()

    def set_trans_mode(self, mode: int) -> bool:
        if mode == 1 and len(self.trans_chinese_list) == 0:
            return False
        if mode == 2 and len(self.trans_romaji_list) == 0:
            return False
        self.trans_mode = mode

        self.restart_thread()
        return True

    def __play_lrc_thread(self, position=None) -> None:
        if position:
            position = position
        else:
            position = self.player.position()
        if position > self.song_time_list[0]:
            for self.order in range(0, self.len_song - 1):
                if position > self.song_time_list[self.len_song - 1]:
                    self.order = self.len_song - 1
                    break
                elif self.song_time_list[self.order] < position < self.song_time_list[self.order + 1]:
                    # self.order -= 1
                    break
            try:
                self.__show_content(self.song_time_list[self.order + 1] - self.player.position())
            except IndexError:
                time.sleep(0.1)
                self.__play_lrc_thread()
                return
        else:
            self.order = 0
            self.__show_content(self.song_time_list[1] - self.player.position())
            self.order += 1  # 第一句的时间需要被忽略

        while self.order < self.len_song - 1:  # 正式进入循环
            self.order += 1
            sleep_time = self.song_time_list[self.order] - self.player.position()
            if sleep_time > 100:
                pass
                time.sleep(sleep_time / 1000 - 0.1)
            if self.is_pause:
                while self.is_pause:  # 当被暂停，让线程停滞
                    time.sleep(0.1)
                continue  # todo 小bug 如果暂停和开始都存在于time.sleep时间 只会影响到下一句（就一句！！！！！呜呜
            elif self.song_time_list[self.order - 1] - self.player.position() > 0 and \
                    self.order > 2 and self.song_time_list[self.order - 1] != self.song_time_list[self.order]:
                # 分别排除了self.order被作为下标为负数的情况 和 歌词文件时间标注重复问题
                print("時間異常")
                time.sleep(0.1)
                self.__play_lrc_thread()
                return
            if self.order + 1 == self.len_song:
                roll_time = 0
            else:
                roll_time = self.song_time_list[self.order + 1] - self.player.position()
            self.__show_content(roll_time)

    def __show_content(self, roll_time: int) -> None:
        order = self.order
        if self.trans_mode == 0:
            print(self.trans_non_list[order])
        elif self.trans_mode == 1:
            print(self.trans_non_list[order])
            print(self.trans_chinese_list[order])
        elif self.trans_mode == 2:
            print(self.trans_non_list[order])
            print(self.trans_romaji_list[order])
        if self.lyrics_window:
            if self.trans_mode == 0:
                self.lyrics_window.set_text(1, self.trans_non_list[order], roll_time)
            elif self.trans_mode == 1:
                self.lyrics_window.set_text(1, self.trans_non_list[order], roll_time)
                self.lyrics_window.set_text(2, self.trans_chinese_list[order], roll_time)
            elif self.trans_mode == 2:
                self.lyrics_window.set_text(1, self.trans_non_list[order], roll_time)
                self.lyrics_window.set_text(2, self.trans_romaji_list[order], roll_time)

    def __load_lrc(self) -> None:
        self._init_lrc_content()
        if not self.lrc_path:
            return
        file_name = ''
        if os.path.splitext(os.path.split(self.lrc_path)[1])[1] == '.krc':
            file_name = os.path.splitext(os.path.split(self.lrc_path)[1])[0]
            krc2lrc(self.lrc_path, file_name + '.lrc')  # krc文件读取转换为lrc
        for line in open(r'' + self.lrc_path, 'r', encoding='utf-8'):
            if re.match(r'\[(\D+):(\S*)]', line):
                text = re.match(r'\[(\D+):(\S*)]', line)
                key = text.group(1)
                context = text.group(2)
                self.information_dict[key] = context
            elif re.match(r'\[\d\d:\d\d.\d+]', line):
                moment = int(line[1:3]) * 60000 + \
                    int(line[4:6]) * 1000 + int(line[7:10])
                context = line[11:]
                self.song_time_list.append(moment)
                self.song_time_list.sort()
                self.trans_non_list.append(context)
        if os.path.exists(file_name + '.lrc'):
            os.remove(file_name + '.lrc')

    def __get_translation(self) -> None:
        translation_dict = json.loads(base64.b64decode(
            (self.information_dict['language'])).decode())
        for language_type_dict in translation_dict['content']:
            if language_type_dict['type'] == 0:  # 罗马音翻译
                for sentence in language_type_dict['lyricContent']:
                    res_sentence = ''
                    for romaji in sentence:
                        res_sentence += romaji
                    self.trans_romaji_list.append(res_sentence)
            if language_type_dict['type'] == 1:  # 中文翻译
                for sentence in language_type_dict['lyricContent']:
                    self.trans_chinese_list.append(sentence[0])


def find_lrc_path(md5_code):
    lrc_file_list = os.listdir(LRC_PATH)
    for lrc_file in lrc_file_list:
        file_name_list = os.path.splitext(lrc_file)[0].split('-')
        lrc_hash = file_name_list[2]
        if md5_code == lrc_hash:
            return LRC_PATH + lrc_file
    else:
        return False


if __name__ == '__main__':
    LRC_PATH = '..\\..\\resource\\Lyric\\'
    print(find_lrc_path('bc37903410ef6f94014563c51da60743'))

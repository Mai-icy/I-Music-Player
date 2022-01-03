# coding : utf-8
import base64
import json
import os
import re
import threading
import time

from PyQt5.QtMultimedia import QMediaPlayer

from common.decode.lyric_decode import KrcFile, LrcFile, MrcFile
from common.path import LRC_PATH
from components.player.music_stream_queue import MusicStreamQueue
from components.player.kill_thread import stop_thread


class LrcPlayer(object):
    def __init__(self, player: QMediaPlayer, playlist: MusicStreamQueue, lyrics_window=None):
        self.lyrics_window = lyrics_window
        self.playlist = playlist
        self.player = player
        self.lrc_file = LrcFile()

        self.trans_mode = 0  # 翻译模式 0为不翻译 1为中文 2为罗马音
        self.is_pause = False

        self.thread_play_lrc = threading.Thread(target=self.__play_lrc_thread)

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
        lrc_path = LRC_PATH + self.playlist.now_song_info["md5"] + '.mrc'
        if os.path.exists(lrc_path):
            suffix = os.path.splitext(os.path.split(lrc_path)[1])[1]
            if suffix == '.krc':
                self.lrc_file = KrcFile(lrc_path)
            elif suffix == '.lrc':
                self.lrc_file = LrcFile(lrc_path)
            elif suffix == '.mrc':
                self.lrc_file = MrcFile(lrc_path)

    def restart_thread(self, position=None) -> None:
        """
        Restart the thread that outputs the lyrics

        :return: None
        """
        self._reload_lrc_data()
        if self.thread_play_lrc.is_alive():
            stop_thread(self.thread_play_lrc)
        if position:
            self.thread_play_lrc = threading.Thread(target=self.__play_lrc_thread, args=(position,))
        else:
            self.thread_play_lrc = threading.Thread(target=self.__play_lrc_thread)
        if self.lrc_file.empty():
            return
        self.thread_play_lrc.start()

    def set_trans_mode(self, mode: int) -> bool:  # todo 反馈
        if mode == 1 and len(self.lrc_file.trans_chinese_dict) == 0:
            return False
        if mode == 2 and len(self.lrc_file.trans_romaji_dict) == 0:
            return False
        self.trans_mode = mode

        # self.restart_thread()
        return True

    def __play_lrc_thread(self, position=None) -> None:
        time.sleep(0.1)
        if position:
            position = position
        else:
            position = self.player.position()

        self.order = self.lrc_file.get_order_position(position)
        if self.order == -1:
            return
        if self.order == 0:
            self.__show_content(self.lrc_file.get_time(1) - self.player.position())
            self.order += 1  # 第一句的时间需要被忽略
        else:
            time_stamp = self.lrc_file.get_time(self.order + 1)
            if time_stamp == -2:
                self.__show_content(0)
            self.__show_content(time_stamp - self.player.position())

        while True:
            sleep_time = self.lrc_file.get_time(self.order + 1) - self.player.position()
            if sleep_time > 100:
                time.sleep(sleep_time / 1000)

            if self.is_pause:
                while self.is_pause:  # 当被暂停，让线程停滞
                    time.sleep(0.1)
                continue  # todo 小bug 如果暂停和开始都存在于time.sleep时间 只会影响到下一句（就一句！！！！！呜呜
            elif self.lrc_file.get_time(self.order) - self.player.position() > 0 and self.order > 2:
                # 分别排除了self.order被作为下标为负数的情况 和 歌词文件时间标注重复问题
                print("時間異常")
                time.sleep(0.1)
                self.__play_lrc_thread()
                return
            self.order += 1

            time_stamp = self.lrc_file.get_time(self.order + 1)
            if time_stamp == -2:
                self.__show_content(0)
                break
            else:
                roll_time = self.lrc_file.get_time(self.order + 1) - self.player.position()
                self.__show_content(roll_time)

    def __show_content(self, roll_time: int) -> None:
        order = self.order
        time_stamp = self.lrc_file.get_time(order)
        if time_stamp == -2:
            return
        print(self.lrc_file.trans_non_dict[time_stamp])
        if self.trans_mode == 1:
            print(self.lrc_file.trans_chinese_dict[time_stamp])
        elif self.trans_mode == 2:
            print(self.lrc_file.trans_romaji_dict[time_stamp])

        if self.lyrics_window:
            self.lyrics_window.set_text(1, self.lrc_file.trans_non_dict[time_stamp], roll_time)
            if self.trans_mode == 1:
                self.lyrics_window.set_text(2, self.lrc_file.trans_chinese_dict[time_stamp], roll_time)
            elif self.trans_mode == 2:
                self.lyrics_window.set_text(2, self.lrc_file.trans_romaji_dict[time_stamp], roll_time)


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

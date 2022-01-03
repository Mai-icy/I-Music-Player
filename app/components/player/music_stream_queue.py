#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import json
import time
import io

from common.path import PLAYLIST_SAVE_PATH
from random import shuffle
from common.song_metadata.read_song_metadata import get_song_metadata, get_album_buffer


class MusicStreamQueue(object):
    def __init__(self, playlist_name):
        self.playlist = {
            "playlistName": playlist_name,
            "modifiedTime": time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime()),
            "songInfo_list": []
        }
        self.now_order = 0  # 当前播放的位置
        self.save_playlist_path = PLAYLIST_SAVE_PATH + '%s.msq'  # 相对位置
        self.now_song_info = {}
        self.msq_name = playlist_name

    def load_playlist(self, msq_name: str, is_random=False) -> bool:
        """
        Load the data of playlist file and save to 'self.playlist'.

        :param msq_name: The file name of playlist.
        :param is_random: Whether to load song info randomly. Default is False
        :return: if successful, return True. If the file does not exist, return False.
        """
        # self.now_song_info = {}
        self.msq_name = msq_name
        self.now_order = 0  # 当前播放的位置
        if os.path.exists(self.save_playlist_path % msq_name):
            with open(self.save_playlist_path % msq_name, 'r', encoding='utf-8') as f:
                del self.playlist
                self.playlist = json.load(f)
                f.close()
            if is_random:
                shuffle(self.playlist["songInfo_list"])
            if len(self.playlist["songInfo_list"]):
                self.now_song_info = self.playlist["songInfo_list"][0]
            else:
                self.now_song_info = None
            return True
        else:
            return False

    def save_playlist(self, save_name: str = None) -> bool:
        """
        Save the playlist to file.

        :param save_name: The name of new file.
        :return: if successful, return True. Conversely, return False.
        """
        if not save_name:
            save_name = self.msq_name
        self.playlist["modifiedTime"] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
        with open(self.save_playlist_path % save_name, 'w', encoding='utf-8') as f:
            json.dump(self.playlist, f, ensure_ascii=False)  # todo 俄语保存为乱码
            f.close()
        return True

    def next_song(self) -> None:
        """
        Point to the next song.

        :return: None
        """
        self.now_order += 1
        if self.now_order >= len(self.playlist["songInfo_list"]):
            self.now_order = 0
        self.now_song_info = self.playlist["songInfo_list"][self.now_order]

    def last_song(self) -> None:
        """
        Point to the last song.

        :return:
        """
        self.now_order -= 1
        if self.now_order <= -1:
            self.now_order = len(self.playlist["songInfo_list"]) - 1
        self.now_song_info = self.playlist["songInfo_list"][self.now_order]

    def get_random_song_queue(self):
        """
        )))))) i don't like it. Maybe I will modify it

        :return:
        """
        new_queue = MusicStreamQueue(self.msq_name)
        new_queue.load_playlist(self.msq_name, True)
        return new_queue

    def append_song2next(self, music_path: str) -> None:
        song_info = get_song_metadata(music_path)
        self.playlist["songInfo_list"].insert(self.now_order + 1, song_info)

    def append_song2end(self, music_path: str) -> None:
        song_info = get_song_metadata(music_path)
        self.playlist["songInfo_list"].append(song_info)

    def delete_song(self, order: int) -> None:
        if order < self.now_order:
            self.now_order -= 1
        self.playlist["songInfo_list"].pop(order)

    def adjust_position(self, ori_pos, res_pos) -> None:
        song_info = self.playlist["songInfo_list"].pop(ori_pos)
        self.playlist["songInfo_list"].insert(res_pos, song_info)
        return

    def get_msq_pic(self) -> io.BytesIO:
        """
        Gets a picture of the most recent song.

        :return: resulting image buffer.
        """
        if len(self.playlist["songInfo_list"]) > 0:
            song_path = self.playlist["songInfo_list"][0]["songPath"]
            buffer = get_album_buffer(song_path)
            return buffer
        else:
            return io.BytesIO()


if __name__ == '__main__':
    modified_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
    print(modified_time)
    PLAYLIST_SAVE_PATH = '..\\..\\resource\\playlist\\'
    a = MusicStreamQueue('new 1')
    print(os.listdir(r'Z:\KuGou\2021.6.21'))
    for file in os.listdir(r'Z:\KuGou\2021.6.21'):
        a.append_song2end('Z:\\KuGou\\2021.6.21\\' + file)
    a.save_playlist()

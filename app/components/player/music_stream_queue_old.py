# -*- coding:utf-8 -*-
import os
import json
# sys.path.append('..')
from random import shuffle
import copy


class MusicStreamQueue(object):
    def __init__(self):
        self.music_stream_list = []
        self.lyric_stream_list = []  # 两个list 一一对应
        self.now_music_path = ''
        self.now_lyric_path = ''
        self.msq_name = ''

        self.now_order = 0  # 当前播放的位置
        self.save_playlist_path = 'playlist\\%s.msq'  # 相对位置

    def load_playlist(self, msq_name: str, is_random=False) -> bool:  # 读取保存的歌单
        self.music_stream_list = []
        self.lyric_stream_list = []  # 两个list初始化
        self.msq_name = msq_name
        if os.path.exists(self.save_playlist_path % msq_name):
            with open(self.save_playlist_path % msq_name, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                f.close()
            if is_random:
                shuffle(data_list)
            for data in data_list:
                self.music_stream_list.append(data['music'])
                self.lyric_stream_list.append(data['lyric'])
            self.now_music_path = self.music_stream_list[0]
            self.now_lyric_path = self.lyric_stream_list[0]
            return True
        else:
            return False

    def save_playlist(self, save_name: str) -> bool:
        save_list = []
        for save_order in range(0, len(self.music_stream_list)):
            save_list.append({'music': self.music_stream_list[save_order], 'lyric': self.lyric_stream_list[save_order]})
        with open(self.save_playlist_path % save_name, 'w', encoding='utf-8') as f:
            json.dump(save_list, f, ensure_ascii=False)
            f.close()
        return True

    def next_song(self) -> None:
        self.now_order += 1
        if self.now_order >= len(self.music_stream_list):
            self.now_order = 0
        self.now_music_path = self.music_stream_list[self.now_order]
        self.now_lyric_path = self.lyric_stream_list[self.now_order]

    def last_song(self) -> None:
        self.now_order -= 1

        if self.now_order <= -1:
            self.now_order = len(self.music_stream_list) - 1
        self.now_music_path = self.music_stream_list[self.now_order]
        self.now_lyric_path = self.lyric_stream_list[self.now_order]

    def get_random_song_queue(self):
        new_queue = MusicStreamQueue()
        new_queue.load_playlist(self.msq_name, True)
        return new_queue

    def append_song2next(self, music_path: str, lrc_path='') -> None:
        self.music_stream_list.insert(self.now_order + 1, music_path)
        self.lyric_stream_list.insert(self.now_order + 1, lrc_path)

    def append_song2end(self, music_path: str, lrc_path='') -> None:
        self.lyric_stream_list.append(lrc_path)
        self.music_stream_list.append(music_path)

    def delete_song(self, order: int) -> None:
        if order < self.now_order:
            self.now_order -= 1
        self.lyric_stream_list.pop(order)
        self.music_stream_list.pop(order)

    def copy(self, play_list) -> None:
        self.music_stream_list = copy.deepcopy(play_list.music_stream_list)
        self.lyric_stream_list = copy.deepcopy(play_list.lyric_stream_list)
        self.lyric_stream_list = copy.deepcopy(play_list.lyric_stream_list)
        self.now_music_path = play_list.now_music_path
        self.now_lyric_path = play_list.now_lyric_path
        self.msq_name = play_list.msq_name
        self.now_order = play_list.now_order  # 当前播放的位置

    def adjust_position(self, ori_pos, res_pos) -> None:
        path_1 = self.music_stream_list.pop(ori_pos)
        path_2 = self.lyric_stream_list.pop(ori_pos)
        self.music_stream_list.insert(res_pos, path_1)
        self.lyric_stream_list.insert(res_pos, path_2)
        return


if __name__ == '__main__':
    '''
        database = db.db_handle.MusicLrcManage('..\\db\\ml_data.db')
        data_list = database.search_table('all')
        qwq = MusicStreamQueue()
        for data in data_list:

            qwq.append_song2next(data['MUSIC_PATH'], data['LRC_PATH'])
        qwq.save_playlist('list_test')
    '''

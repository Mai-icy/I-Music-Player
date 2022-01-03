#!/usr/bin/python
# -*- coding:utf-8 -*-
import copy
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from components.player.lyric_player import LrcPlayer
from components.player.music_stream_queue import MusicStreamQueue


class MediaPlayer(QMediaPlayer):
    slider_reset_signal = pyqtSignal(str)

    def __init__(self, lyrics_window, parent=None):
        super(MediaPlayer, self).__init__(parent)
        # 读取文件
        self.playlist = MusicStreamQueue('temporary')
        self.backup_play_stream = self.playlist

        self.lrc_play = LrcPlayer(self, self.playlist, lyrics_window)
        self.play_stream_mode = 0  # 0顺序播放 1随机播放 2单曲循环

        # self.setMedia(QMediaContent(QUrl(self.playlist.now_song_info['son gPath'].replace('\\', "/"))))

        self.stateChanged.connect(self.__play_over_event)  # 播放完毕连接的函数

    def load_playlist(self, play_stream: MusicStreamQueue):
        """
        Reset the play stream.

        :param play_stream:
        :return:
        """
        self.stop()
        self.playlist = play_stream
        self.backup_play_stream = self.playlist
        self.lrc_play.load_playlist(self.playlist)
        self.setMedia(QMediaContent(QUrl(self.playlist.now_song_info['songPath'].replace('\\', "/"))))
        self.lrc_play.restart_thread()

    def play_pause_player(self) -> None:
        """
        Pause if it is playing, and start if it is paused

        :return: None
        """
        if self.state() == 1:
            self.pause()
            self.lrc_play.is_pause = True
        elif self.state() == 2 or self.state() == 0:
            self.play()
            self.lrc_play.is_pause = False

    def next_song(self) -> None:
        """
        Play the next song in queue and emit reset slider signal

        :return: None
        """
        self.playlist.next_song()
        self.setMedia(QMediaContent(QUrl(self.playlist.now_song_info['songPath'].replace('\\', "/"))))
        self.slider_reset_signal.emit('')
        self.play_pause_player()
        self.lrc_play.restart_thread()

    def last_song(self) -> None:
        """
        Play the last song in queue and emit reset slider signal

        :return: None
        """
        self.playlist.last_song()
        self.setMedia(QMediaContent(QUrl(self.playlist.now_song_info['songPath'].replace('\\', "/"))))
        self.slider_reset_signal.emit('')
        self.play_pause_player()
        self.lrc_play.restart_thread()

    def set_play_stream_mode(self, mode: int) -> None:  # 0顺序播放 1随机播放 2单曲循环
        if self.play_stream_mode == 1 and mode != 1:
            now_song_info = self.playlist.now_song_info

            self.playlist = self.backup_play_stream.get_random_song_queue()  # todo 修改获取随机的方法

            self.playlist.playlist["songInfo_list"].remove(now_song_info)
            self.playlist.playlist["songInfo_list"].insert(
                0, now_song_info)  # 把当前播放的曲目置顶
            # 播放列表变化 变成新生成的随机列表
            self.lrc_play.play_stream = self.playlist  # 同步到歌词播放的play_stream
        elif self.play_stream_mode != 1 and mode == 1:
            self.playlist = copy.deepcopy(
                self.backup_play_stream)  # todo 修改为重新加载
            # 播放列表变化 变回原来的列表
            self.lrc_play.play_stream = self.playlist  # 同步到歌词播放的play_stream
        self.play_stream_mode = mode

    def set_position(self, position: int) -> None:  # position为毫秒数
        self.setPosition(position)
        # self.lrc_play.restart_thread(position)
        self.lrc_play.restart_thread()

    def __play_over_event(self) -> None:
        if self.state() == 0 and self.mediaStatus() == 7:  # 歌曲播放完毕
            if self.play_stream_mode == 2:
                self.play_pause_player()
                self.lrc_play.restart_thread()  # 确保歌词重新打开
            else:
                self.next_song()
        else:  #
            return

    def set_lyrics_window(self, lyrics_window):
        # todo
        self.lrc_play.lyrics_window = lyrics_window


if __name__ == '__main__':
    pass

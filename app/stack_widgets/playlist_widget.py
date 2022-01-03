#!/usr/bin/env python
# coding=utf-8
import sys
import time
import os

from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import common.song_metadata as sm
from ui_source.PlayListWidget import Ui_PlayListWidget
from components.player.music_stream_queue import MusicStreamQueue
from common.path import PLAYLIST_SAVE_PATH
from common.song_metadata.read_song_metadata import get_md5


class PlayListWidget(QWidget, Ui_PlayListWidget):
    rename_signal = pyqtSignal(str)

    def __init__(self, playlist_name, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        # self.playlist_name = playlist_name
        self.playlist = MusicStreamQueue(playlist_name)

        self._init_setting()
        self._init_signal()

    def _init_signal(self):
        self.add_song_button.clicked.connect(self.add_song_event)
        self.rename_button.clicked.connect(self.rename_event)

    def _init_setting(self):
        self.setMouseTracking(True)
        self.setMinimumSize(self.get_table_widget_size(self.song_data_tablewidget))  # 设置最小值

    def resize_widget(self):
        size = self.get_table_widget_size(self.song_data_tablewidget)
        self.setMinimumSize(size)
        self.song_data_tablewidget.setMinimumSize(QSize(size.width(), size.height() - 238))  # 使QTableWidget展开

    def load_playlist_file(self, msq_name):
        if self.playlist.load_playlist(msq_name):
            msq_path = PLAYLIST_SAVE_PATH + msq_name + '.msq'
            md5 = get_md5(msq_path)
            self.playlist_cover_label.setScaledContents(True)
            if os.path.exists(PLAYLIST_SAVE_PATH + f"pic\\{md5}.png"):
                pix = Image.open(PLAYLIST_SAVE_PATH + f"pic\\{md5}.png").toqpixmap()
                self.pic_label.setPixmap(pix)
            else:
                buffer = self.playlist.get_msq_pic()
                if buffer.getvalue():
                    pix = Image.open(buffer).toqpixmap()
                    self.playlist_cover_label.setPixmap(pix)
                else:
                    pass
                    # todo 设置空图
            self.playlist_title_label.setText(msq_name)
            self.__refresh_table_widget()

    @staticmethod
    def get_table_widget_size(table):
        w = table.verticalHeader().width() + 0  # 表头无高度
        for i in range(table.columnCount()):
            w += table.columnWidth(i)
        h = table.horizontalHeader().height() + 4
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        h += 238  # 添加了表格上面控件的长度
        return QtCore.QSize(w, h)

    def __refresh_table_widget(self):
        self.song_data_tablewidget.load_playlist(self.playlist)
        self.resize_widget()

    def add_song_event(self):
        file_name_list = QFileDialog.getOpenFileNames(self, u"打开文件", "", "Music files(*.mp3 *.flac)")[0]
        for file_path in file_name_list:
            self.playlist.append_song2end(file_path)
        self.__refresh_table_widget()
        self.save_event()

    def save_event(self):
        self.playlist.save_playlist()

    def rename_event(self):
        self.rename_signal.emit(self.playlist.msq_name)


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = PlayListWidget("test")
    myWin.show()
    sys.exit(app.exec_())

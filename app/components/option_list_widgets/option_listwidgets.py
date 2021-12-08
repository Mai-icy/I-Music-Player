# encoding:utf-8

import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from components.option_list_widgets.option_listwidget_items import Ui_Form


class LeftListWidget(QListWidget):
    def __init__(self, parent=None):
        super(LeftListWidget, self).__init__(parent)
        self._init_data()
        self._init_base_item()

    def itemClicked(self, item: QListWidgetItem) -> None:
        pass

    def click_event(self):
        index = self.main_window.left_sidebar_listwidget.currentIndex().row()
        if index == 0:
            pass
        elif index == self._play_list_item_index:
            self.unfold_play_list_event()
        elif index == self.tool_box_item_index:
            self.unfold_tool_list_event()
        elif index == self.download_api_item_index:
            self.unfold_api_list_event()
        elif self._play_list_item_index < index < self.tool_box_item_index:  # play_list_item内事件
            inner_index = index - self._play_list_item_index
            # 测试用
            if inner_index == 1:
                self.main_window.stack_scrollarea.takeWidget()
                self.main_window.stack_scrollarea.setWidget(self.main_window.song_list_widget)
        elif self.tool_box_item_index < index < self.download_api_item_index:
            inner_index = index - self.tool_box_item_index
            # 测试用
            if inner_index == 1:
                self.main_window.stack_scrollarea.takeWidget()
                self.main_window.stack_scrollarea.setWidget(self.main_window.kugou_api_widget)

        elif index > self.download_api_item_index:
            pass

    def _init_data(self):
        self._local_music_item_index = 0
        self._local_lyric_item_index = 1
        self._play_list_item_index = 2
        self.tool_box_item_index = 3
        self.download_api_item_index = 4

        self.item_num_play_list = 0  # 需要读取并会被修改
        self.item_num_tool_box = 2
        self.item_num_download_api = 2

        self.is_unfold_play_list = False
        self.is_unfold_tool_box = False
        self.is_unfold_download_api = False

    def _init_base_item(self):
        init_up_list = ['本地歌曲', '本地歌词']
        for up_item_text in init_up_list:
            base_item = QListWidgetItem()
            base_item.setSizeHint(QSize(30, 30))
            base_item.setFont(QFont("黑体", 15))
            base_item.setText(up_item_text)
            base_item.setIcon(QIcon(r'Z:\MMusicPlayer合作文件夹\images\2222.png'))
            self.main_window.left_sidebar_listwidget.addItem(base_item)
        init_father_list = ['我的歌单', '工具箱', '歌词下载']
        for father_item_text in init_father_list:
            father_item = QListWidgetItem()
            father_item.setSizeHint(QSize(30, 30))
            self.main_window.left_sidebar_listwidget.addItem(father_item)
            self.main_window.left_sidebar_listwidget.setItemWidget(father_item, Ui_Form(father_item_text))

    def unfold_tool_list_event(self):
        if self.is_unfold_tool_box:
            self.is_unfold_tool_box = False
            for i in range(self.item_num_tool_box):
                self.__delete_item(self.tool_box_item_index + 1)
            self.download_api_item_index -= self.item_num_tool_box
        else:
            self.is_unfold_tool_box = True
            self.download_api_item_index += self.item_num_tool_box
            for i in range(self.item_num_tool_box):
                item = QListWidgetItem()
                item.setSizeHint(QSize(30, 30))
                item.setText('工具文本')

                self.main_window.left_sidebar_listwidget.insertItem(self.tool_box_item_index + 1, item)

    def unfold_play_list_event(self):
        if self.is_unfold_play_list:
            self.is_unfold_play_list = False
            for i in range(self.item_num_play_list):
                self.__delete_item(self._play_list_item_index + 1)
            self.tool_box_item_index -= self.item_num_play_list
            self.download_api_item_index -= self.item_num_play_list
        else:
            self.is_unfold_play_list = True
            self.item_num_play_list = len(os.listdir(r'..\resource\playlist'))  # 获取歌单的数量
            self.tool_box_item_index += self.item_num_play_list
            self.download_api_item_index += self.item_num_play_list
            for i in range(self.item_num_play_list):
                item = QListWidgetItem()
                item.setSizeHint(QSize(30, 30))
                item.setText('歌单文本')

                self.main_window.left_sidebar_listwidget.insertItem(self._play_list_item_index + 1, item)

    def unfold_api_list_event(self):
        if self.is_unfold_download_api:
            self.is_unfold_download_api = False
            for i in range(self.item_num_download_api):
                self.__delete_item(self.download_api_item_index + 1)
        else:
            self.is_unfold_download_api = True
            for i in range(self.item_num_download_api):
                item = QListWidgetItem()
                item.setSizeHint(QSize(30, 30))
                item.setText('api文本')

                self.main_window.left_sidebar_listwidget.insertItem(self.download_api_item_index + 1, item)

    def __delete_item(self, r):
        self.main_window.left_sidebar_listwidget.removeItemWidget(self.main_window.left_sidebar_listwidget.takeItem(r))


#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from components.option_list_widgets.option_listwidget_items import PlaylistItemsWidget, PlaylistItemWidget
from common.path import PLAYLIST_SAVE_PATH
from components.player.music_stream_queue import MusicStreamQueue
from dialog_box.single_input_dialog import SingleInputDialog
from components.mask_widget.mask_widget import MaskWidget
import stack_widgets


class LeftListWidget(QListWidget):
    """
    Toolbar on the left. ListWidget emulates a tree structure.
    """
    play_music_signal = pyqtSignal(MusicStreamQueue)

    def __init__(self, main_widget, parent=None):
        super(LeftListWidget, self).__init__(parent)
        self.main_widget = main_widget
        self.mask = MaskWidget(self.main_widget)
        self.mask.close()
        self._init_data()
        self._init_base_item()
        self._init_widget()
        self._init_signal()

    def _init_widget(self):
        """
        初始化widget窗口，工具栏内的playlist_widget，metadata_widget，
        kugou_api_widget都由该类管辖。

        :return:
        """
        self.__load_playlist_folder()

        self.playlist_widget = stack_widgets.PlayListWidget("N/A")
        self.metadata_widget = stack_widgets.MetadataWidget()

        self.kugou_api_widget = stack_widgets.KugouApiWidget()
        self.kugou_api_widget.search_data_tablewidget.is_enter_event = False

    def _init_signal(self):
        """
        连接负责的内置窗口widget的简单信号。

        :return:
        """
        self.itemClicked.connect(self.item_click_event)
        self.playlist_widget.song_data_tablewidget.double_click_signal.connect(
            self.song_double_click_event)
        self.playlist_widget.rename_signal.connect(self.rename_playlist)

    def __load_playlist_folder(self):
        """
        加载歌单文件夹内的歌单文件，存入playlist_file_list成员。

        :return:
        """
        if os.path.exists(PLAYLIST_SAVE_PATH + 'index'):
            file = open(PLAYLIST_SAVE_PATH + 'index', "r", encoding="utf-8")
            index_list = eval(file.read())
            file.close()
            new_playlist = [x for x in os.listdir(
                PLAYLIST_SAVE_PATH) if x not in index_list]
            new_playlist.remove('index')
            index_list.extend(new_playlist)

            delete_playlist = [
                x for x in index_list if x not in os.listdir(PLAYLIST_SAVE_PATH)]
            for i in delete_playlist:
                index_list.remove(i)
        else:
            index_list = os.listdir(PLAYLIST_SAVE_PATH)
        with open(PLAYLIST_SAVE_PATH + 'index', "w", encoding="utf-8") as f:
            f.write(str(index_list))
            f.close()

        self.playlist_file_list = index_list
        self.playlist_file_list = list(
            map(lambda x: os.path.splitext(x)[0], self.playlist_file_list))
        self.__item_num_playlist = len(self.playlist_file_list)

    def _init_data(self):
        """
        初始化关于模拟树形结构的内部成员参数

        :return:
        """
        self.__local_music_item_index = 0
        self.__local_lyric_item_index = 1
        self.__play_list_item_index = 2
        self.__tool_box_item_index = 3

        self.__item_num_playlist = 0  # 需要读取并会被修改
        self.__item_num_tool_box = 2

        self.__is_unfold_play_list = False
        self.__is_unfold_tool_box = False

    def _init_base_item(self):
        init_up_list = ['本地歌曲', '本地歌词']
        for up_item_text in init_up_list:
            base_item = QListWidgetItem()
            base_item.setSizeHint(QSize(30, 30))
            base_item.setFont(QFont("黑体", 15))
            base_item.setText(up_item_text)
            base_item.setIcon(QIcon(r'Z:\MMusicPlayer合作文件夹\images\2222.png'))
            self.addItem(base_item)

        playlist_item = QListWidgetItem()
        playlist_item.setSizeHint(QSize(40, 40))
        widget = PlaylistItemsWidget('我的歌单')
        widget.pushButton.clicked.connect(self.create_new_playlist_event)
        self.addItem(playlist_item)
        self.setItemWidget(playlist_item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(40, 40))
        item.setText('工具箱')
        self.addItem(item)

    def __unfold_tool_list_event(self):
        if self.__is_unfold_tool_box:
            self.__is_unfold_tool_box = False
            for i in range(self.__item_num_tool_box):
                self.__delete_item(self.__tool_box_item_index + 1)
        else:
            self.__is_unfold_tool_box = True
            text_list = ["酷狗歌词api", "元数据补全窗口"]
            for i in range(self.__item_num_tool_box):
                item = QListWidgetItem()
                item.setSizeHint(QSize(30, 30))
                item.setText(text_list[i])

                self.insertItem(self.__tool_box_item_index + 1, item)

    def __unfold_play_list_event(self):
        if self.__is_unfold_play_list:
            self.__is_unfold_play_list = False
            for i in range(self.__item_num_playlist):
                self.__delete_item(self.__play_list_item_index + 1)
            self.__tool_box_item_index -= self.__item_num_playlist
        else:
            self.__is_unfold_play_list = True
            self.__tool_box_item_index += self.__item_num_playlist

            for msq_name in reversed(self.playlist_file_list):
                self.__add_playlist_item(
                    msq_name, self.__play_list_item_index + 1)

    def __add_playlist_item(self, text, row):
        item = QListWidgetItem()
        item.setSizeHint(QSize(30, 30))
        item.setText(text)
        widget = PlaylistItemWidget(text)
        widget.remove_signal.connect(self.remove_playlist)
        widget.rename_signal.connect(self.rename_playlist)
        self.insertItem(row, item)
        self.setItemWidget(item, widget)

    def remove_playlist(self, item_name: str):
        operate_index_file(
            lambda index_list: index_list.remove(
                item_name + '.msq'))

        os.remove(PLAYLIST_SAVE_PATH + item_name + '.msq')
        self.playlist_file_list.remove(item_name)
        self.__item_num_playlist -= 1
        self.__tool_box_item_index -= 1
        if item_name == self.playlist_widget.playlist.msq_name:
            self.main_widget.stack_scrollarea.takeWidget()
        for row in range(
                self.__play_list_item_index + 1,
                self.__tool_box_item_index + 1):
            item = self.item(row)
            if item.text() == item_name:
                self.__delete_item(row)
                return

    def rename_playlist(self, item_name: str):
        for row in range(
                self.__play_list_item_index + 1,
                self.__tool_box_item_index):
            item = self.item(row)
            if item.text() == item_name:
                self.setCurrentItem(item)
                self.item_click_event()
        create_new_dialog = SingleInputDialog(
            self, title_text="重命名歌单", edit_text="请输入歌单名")
        self.mask = MaskWidget(self.main_widget)
        self.mask.show()
        create_new_dialog.show()
        create_new_dialog.done_signal.connect(self.__rename_playlist_done)

    def __rename_playlist_done(self, text):
        self.mask.close()
        if text:
            def rename_operate(index_list: list, is_suffix=True):
                if is_suffix:
                    index = index_list.index(
                        self.playlist_widget.playlist.msq_name + '.msq')
                else:
                    index = index_list.index(
                        self.playlist_widget.playlist.msq_name)
                index_list.pop(index)
                if is_suffix:
                    index_list.insert(index, text + '.msq')
                else:
                    index_list.insert(index, text)
            operate_index_file(rename_operate)

            os.rename(
                PLAYLIST_SAVE_PATH +
                self.playlist_widget.playlist.msq_name +
                '.msq',
                PLAYLIST_SAVE_PATH +
                text +
                '.msq')
            rename_operate(self.playlist_file_list, is_suffix=False)
            self.currentItem().setText(text)
            self.playlist_widget.playlist_title_label.setText(text)

    def __delete_item(self, r):
        self.removeItemWidget(self.takeItem(r))

    def item_click_event(self) -> None:
        index = self.currentIndex().row()
        if index == 0:
            pass
        elif index == self.__play_list_item_index:
            self.__unfold_play_list_event()
        elif index == self.__tool_box_item_index:
            self.__unfold_tool_list_event()

        elif self.__play_list_item_index < index < self.__tool_box_item_index:  # play_list_item内事件
            inner_index = index - self.__play_list_item_index
            self.main_widget.stack_scrollarea.takeWidget()
            self.playlist_widget.load_playlist_file(
                self.playlist_file_list[inner_index - 1])
            self.main_widget.stack_scrollarea.setWidget(self.playlist_widget)

        elif self.__tool_box_item_index < index:
            inner_index = index - self.__tool_box_item_index
            # 测试用
            if inner_index == 1:
                self.main_widget.stack_scrollarea.takeWidget()
                self.main_widget.stack_scrollarea.setWidget(
                    self.kugou_api_widget)
            if inner_index == 2:
                self.main_widget.stack_scrollarea.takeWidget()
                self.main_widget.stack_scrollarea.setWidget(
                    self.metadata_widget)
        elif index > self.__tool_box_item_index:
            pass

    def create_new_playlist_event(self):
        create_new_dialog = SingleInputDialog(
            self, title_text="新建歌单", edit_text="请输入歌单名")
        self.mask = MaskWidget(self.main_widget)
        self.mask.show()
        create_new_dialog.show()
        create_new_dialog.done_signal.connect(self.__create_new_playlist_done)

    def __create_new_playlist_done(self, text):
        self.mask.close()
        if text:
            operate_index_file(
                lambda index_list: index_list.insert(
                    0, text + '.msq'))
            self.__item_num_playlist += 1
            if not self.__is_unfold_play_list:
                self.__unfold_play_list_event()
            else:
                self.__tool_box_item_index += 1
            self.__add_playlist_item(text, self.__play_list_item_index + 1)
            new_playlist = MusicStreamQueue(text)
            new_playlist.save_playlist()
            self.playlist_file_list.insert(0, text)

    def song_double_click_event(self, row):
        """
        双击音乐表格，发送一个播放列表的信号给主窗口，以供播放音乐。

        :param row: 点击的行
        :return:
        """
        playlist = MusicStreamQueue("N/A")
        playlist.load_playlist(self.playlist_widget.playlist.msq_name)
        playlist.now_order = row - 1
        playlist.next_song()
        self.play_music_signal.emit(playlist)


def operate_index_file(func):
    file = open(PLAYLIST_SAVE_PATH + 'index', "r", encoding="utf-8")
    index_list = eval(file.read())
    file.close()
    func(index_list)
    with open(PLAYLIST_SAVE_PATH + 'index', "w", encoding="utf-8") as f:
        f.write(str(index_list))
        f.close()

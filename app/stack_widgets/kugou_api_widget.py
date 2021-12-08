# encoding: utf-8
import sys
import time
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ui_source.KugouApiWidget import Ui_KugouApiWidget
from common.api.kugou_api import KuGouApi


class KugouApiWidget(QWidget, Ui_KugouApiWidget):
    scroll2upSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(KugouApiWidget, self).__init__(parent)
        self.setupUi(self)
        self.setMinimumSize(self.__get_table_widget_size())
        self._init_context()
        self._init_signal_connect()
        self.kugou_api = KuGouApi()
        self.page = 0
        self.keyword = ''
        self.select_row = None

        self.path_list = [' 酷狗搜索']  # 位于上端的由‘->’连接的部分

    def _init_signal_connect(self):
        self.search_button.clicked.connect(self.search_event)
        self.undo_button.clicked.connect(self.undo_event)
        self.redo_button.clicked.connect(self.redo_event)
        self.next_page_button.clicked.connect(self.next_page_event)
        self.last_page_button.clicked.connect(self.last_page_event)
        self.search_data_tablewidget.double_click_signal.connect(self.search_id_key_event)

    def _init_context(self):
        self.page_label.setText('第0页')
        self.search_path_label.setText(' 酷狗搜索 -> ')
        self.search_data_tablewidget.setAcceptDrops(False)
        self.search_data_tablewidget.is_enter_event = False
        self.next_page_button.setEnabled(False)
        self.last_page_button.setEnabled(False)

    def __get_table_widget_size(self):
        w = self.search_data_tablewidget.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.search_data_tablewidget.columnCount()):
            w += self.search_data_tablewidget.columnWidth(i)
        h = self.search_data_tablewidget.horizontalHeader().height() + 4
        for i in range(self.search_data_tablewidget.rowCount()):
            h += self.search_data_tablewidget.rowHeight(i)
        h += 131  # 添加了表格上面控件的长度
        return QtCore.QSize(525, h)

    # region 加载表格内容函数
    def load_music_search_data(self, res_data: list):
        self.search_data_tablewidget.setRowCount(0)
        self.search_data_tablewidget.clearContents()

        total_num = len(res_data)
        self.search_data_tablewidget.setRowCount(total_num)

        for data_index in range(0, total_num):
            song_name = res_data[data_index][0]
            singer_name = res_data[data_index][1]
            album_name = res_data[data_index][2]
            duration = res_data[data_index][3]
            text_duration = '%d:%d%d' % (duration // 60, duration % 60 // 10, duration % 10)

            item = QTableWidgetItem()
            item.setText(song_name)
            self.search_data_tablewidget.setItem(data_index, 0, item)
            item = QTableWidgetItem()
            item.setText(singer_name)
            self.search_data_tablewidget.setItem(data_index, 1, item)
            item = QTableWidgetItem()
            item.setText(album_name)
            self.search_data_tablewidget.setItem(data_index, 2, item)
            item = QTableWidgetItem()
            item.setText(text_duration)
            self.search_data_tablewidget.setItem(data_index, 3, item)

        self.setMinimumSize(self.__get_table_widget_size())

    def load_lrc_search_data(self, res_data):
        self.search_data_tablewidget.setRowCount(0)
        self.search_data_tablewidget.clearContents()
        total_num = len(res_data)
        self.search_data_tablewidget.setRowCount(total_num)
        for data_index in range(0, total_num):
            product_from = res_data[data_index][0]
            uploader_name = res_data[data_index][1]
            score = str(res_data[data_index][2])
            duration = res_data[data_index][3] // 1000
            text_duration = '%d:%d%d' % (duration // 60, duration % 60 // 10, duration % 10)
            item = QTableWidgetItem()
            item.setText(product_from)
            self.search_data_tablewidget.setItem(data_index, 0, item)
            item = QTableWidgetItem()
            item.setText(uploader_name)
            self.search_data_tablewidget.setItem(data_index, 1, item)
            item = QTableWidgetItem()
            item.setText(score)
            self.search_data_tablewidget.setItem(data_index, 2, item)
            item = QTableWidgetItem()
            item.setText(text_duration)
            self.search_data_tablewidget.setItem(data_index, 3, item)
        self.setMinimumSize(self.__get_table_widget_size())
    # endregion

    # region 按键相关事件
    def search_event(self):
        self.search_data_tablewidget.set_music_search_table()
        self.keyword = self.search_lineEdit.text()
        self.page = 1
        if not self.keyword:
            return
        _, next_res_data = self.kugou_api.search_hash(self.keyword, 2, is_change_hash=False)
        total_num, res_data = self.kugou_api.search_hash(self.keyword)
        self.load_music_search_data(res_data)
        if len(self.path_list) > 1:
            self.path_list = [' 酷狗搜索']
        self.path_list.append('%s搜索结果, 共%d个' % (self.keyword, total_num))
        self.search_path_label.setText(' -> '.join(self.path_list))
        self.page_label.setText('第1页')

        self.last_page_button.setEnabled(False)
        if len(next_res_data) < 2:
            self.next_page_button.setEnabled(False)
        else:
            self.next_page_button.setEnabled(True)

    def search_id_key_event(self, e_row):
        self.select_row = e_row
        if self.kugou_api.id_key_list:  # 搜索歌曲时，结果为False
            self.download_lyric_event(e_row)
        else:
            self.search_data_tablewidget.set_lrc_search_table()
            res_data = self.kugou_api.search_id_key(e_row)

            song_name = self.kugou_api.hash_list[e_row][0]

            self.path_list.append('歌曲 %s 歌词搜索结果' % song_name)

            self.search_path_label.setText(' -> '.join(self.path_list))

            self.load_lrc_search_data(res_data)
            self.page_label.setText('第1页')
            self.next_page_button.setEnabled(False)
            self.last_page_button.setEnabled(False)

    def download_lyric_event(self, e_row):
        self.kugou_api.download_krc_or_lrc(e_row)
        print('下载成功')

    def next_page_event(self):
        next_res_data = ()
        if self.kugou_api.id_key_list:  # 搜索歌曲时，结果为False
            pass
        else:
            self.page += 1
            _, next_res_data = self.kugou_api.search_hash(self.keyword, self.page + 1, is_change_hash=False)
            _, res_data = self.kugou_api.search_hash(self.keyword, self.page)
            self.load_music_search_data(res_data)
            self.page_label.setText('第%d页' % self.page)

        if len(next_res_data) < 2:
            self.next_page_button.setEnabled(False)
        self.last_page_button.setEnabled(True)
        self.scroll2upSignal.emit('')

    def last_page_event(self):
        if self.kugou_api.id_key_list:  # 搜索歌曲时，结果为False
            pass
        else:
            self.page -= 1
            _, res_data = self.kugou_api.search_hash(self.keyword, self.page)
            self.load_music_search_data(res_data)
            self.page_label.setText('第%d页' % self.page)

        if self.page == 1:
            self.last_page_button.setEnabled(False)
        self.scroll2upSignal.emit('')

    def redo_event(self):
        if len(self.path_list) == 1:
            self.search_lineEdit.setText(self.keyword)
            self.search_event()
        elif len(self.path_list) == 2:
            self.search_id_key_event(self.select_row)

    def undo_event(self):
        if len(self.path_list) == 1:
            return
        self.path_list.pop()
        if len(self.path_list) == 1:
            self.search_data_tablewidget.set_music_search_table()
            self.next_page_button.setEnabled(False)
            self.last_page_button.setEnabled(False)
            self.search_data_tablewidget.clearContents()
            self.search_data_tablewidget.setRowCount(0)
        elif len(self.path_list) == 2:
            self.search_event()
        self.search_path_label.setText(' -> '.join(self.path_list))
        self.scroll2upSignal.emit('')
    # endregion


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = KugouApiWidget()
    myWin.show()
    sys.exit(app.exec_())


















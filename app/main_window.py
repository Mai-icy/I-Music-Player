# coding:utf-8
import random
import sys
import time
import os
from copy import deepcopy

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_source.MainWindow import Ui_MainWindow
import stack_widgets
import components.player as player

from components.option_list_widgets.option_listwidget_items import Ui_Form
from components.lyrics_window.lyrics_window import LyricsWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint)
        self.c_list_widget = LeftListWidget(self)
        self._init_widget()
        self._init_music_player()
        self._init_signal_connect()

        self._init_test()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # 初始化无边框窗口拉伸拖动
        self.set_mouse_track()
        self._initDrag()
        self.installEventFilter(self)  # 初始化事件过滤器
        self.setMouseTracking(True)

    def _init_widget(self):
        self.song_list_widget = stack_widgets.PlayListWidget()
        a = player.MusicStreamQueue('')
        a.load_playlist('new 1')
        self.song_list_widget.song_data_tablewidget.load_playlist(a)
        self.song_list_widget.resize_widget()

        self.kugou_api_widget = stack_widgets.KugouApiWidget()
        self.kugou_api_widget.search_data_tablewidget.is_enter_event = False

        self.metadata_widget = stack_widgets.MetadataWidget()

    def _init_signal_connect(self):
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(self.showMinimized)  # 小化到任务栏
        self.song_list_widget.song_data_tablewidget.double_click_signal.connect(self.double_click_event)
        self.kugou_api_widget.scroll2upSignal.connect(self.scroll_up_event)
        self.metadata_widget.double_click_signal.connect(self.metadata_double_click_event)

    # region Widget相关事件连接
    def double_click_event(self, row):
        self.song_list_widget.song_data_tablewidget.playlist.now_order = row - 1
        self.song_list_widget.song_data_tablewidget.playlist.next_song()  # 设置成员变量
        self.load_play_list(self.song_list_widget.song_data_tablewidget.playlist)

    def metadata_double_click_event(self, item):
        print(item.text())
    # endregion
    
    def scroll_up_event(self):
        self.stack_scrollarea.ensureVisible(0, 0)

    # region 无边框窗口拉伸拖动相关
    def set_mouse_track(self):  # 设置鼠标跟踪
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.frame.setMouseTracking(True)
        self.below_bar_frame.setMouseTracking(True)
        self.left_sidebar_listwidget.setMouseTracking(True)
        self.stack_scrollarea.setMouseTracking(True)
        self.scrollAreaWidgetContents.setMouseTracking(True)

        # 设置鼠标跟踪判断扳机默认值

    def _initDrag(self):
        self._move_drag = False
        self._bottom_right_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._upper_drag = False
        self._bottom_left_drag = False
        self._upper_left_drag = False
        self._upper_right_drag = False

        # 鼠标释放后，各扳机复位

    def mouseReleaseEvent(self, QMouseEvent):
        self._move_drag = False
        self._bottom_right_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._upper_drag = False
        self._bottom_left_drag = False
        self._upper_left_drag = False
        self._upper_right_drag = False

        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式

    def eventFilter(self, obj, event):

        if isinstance(event, QEnterEvent):
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        return super(MainWindow, self).eventFilter(obj, event)

        # 自定义窗口调整大小范围

    def resizeEvent(self, QResizeEvent):
        self._right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5) for y in
                            range(5, self.height() - 5)]
        self._bottom_rect = [QPoint(x, y) for x in range(5, self.width() - 5) for y in
                             range(self.height() - 5, self.height() + 5)]
        self._bottom_right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5) for y in
                                   range(self.height() - 5, self.height() + 5)]
        self._left_rect = [QPoint(x, y) for x in range(-5, 5) for y in range(5, self.height() - 5)]
        self._upper_rect = [QPoint(x, y) for x in range(5, self.width() - 5) for y in range(-5, 5)]
        self._bottom_left_rect = [QPoint(x, y) for x in range(-5, 5) for y in
                                  range(self.height() - 5, self.height() + 5)]
        self._upper_right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5) for y in range(-5, 5)]
        self._upper_left_rect = [QPoint(x, y) for x in range(-5, 5) for y in range(-5, 5)]

    def mousePressEvent(self, event):  # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_right_rect):
            # 鼠标左键点击右下角边界区域
            self._bottom_right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._left_rect):
            # 鼠标左键点击左侧边界区域
            self._left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._upper_rect):
            # 鼠标左键点击上侧边界区域
            self._upper_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_left_rect):
            # 鼠标左键点击左下角边界区域
            self._bottom_left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._upper_right_rect):
            # 鼠标左键点击右上角边界区域
            self._upper_right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._upper_left_rect):
            # 鼠标左键点击左下角角边界区域
            self._upper_left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos().x() > 5 and event.pos().x() < self.width() - 5
                                                    and event.pos().y() > 5 and event.pos().y() < self.frame.height()):
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):  # 重写鼠标移动的事件
        pos = QMouseEvent.pos()
        # 判断鼠标位置切换鼠标手势
        if (pos in self._bottom_right_rect) or (pos in self._upper_left_rect):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif (pos in self._bottom_rect) or (pos in self._upper_rect):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif (pos in self._right_rect) or (pos in self._left_rect):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif (pos in self._bottom_left_rect) or (pos in self._upper_right_rect):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # 更改窗口大小
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(pos.x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), pos.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_right_drag:
            # 右下角同时调整高度和宽度
            self.resize(pos.x(), pos.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._left_drag:
            # 左侧调整宽度
            if not (self.width() == self.minimumWidth() and pos.x() > 0):
                self.setGeometry(
                    self.geometry().x() + pos.x(),
                    self.geometry().y(),
                    self.width() - pos.x(),
                    self.height())
                QMouseEvent.accept()
        elif Qt.LeftButton and self._upper_drag:
            # 上侧调整高度
            if not ((self.height() == self.minimumHeight() and pos.y() > 0)
                    or (self.height() == self.maximumHeight() and pos.y() < 0)):
                self.setGeometry(
                    self.geometry().x(),
                    self.geometry().y() + pos.y(),
                    self.width(),
                    self.height() - pos.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_left_drag:
            # 左下角同时调整高度和宽度
            if not (self.width() == self.minimumWidth() and pos.x() > 0):
                self.setGeometry(
                    self.geometry().x() + pos.x(),
                    self.geometry().y(),
                    self.width() - pos.x(),
                    pos.y())
                QMouseEvent.accept()
        elif Qt.LeftButton and self._upper_right_drag:
            # 右上角同时调整高度和宽度
            if not ((self.height() == self.minimumHeight() and pos.y() > 0)
                    or (self.height() == self.maximumHeight() and pos.y() < 0)):
                self.setGeometry(
                    self.geometry().x(),
                    self.geometry().y() + pos.y(),
                    pos.x(),
                    self.height() - pos.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._upper_left_drag:
            # 左上角同时调整高度和宽度
            if not ((self.height() == self.minimumHeight() and pos.y() > 0)
                    or (self.height() == self.maximumHeight() and pos.y() < 0)):
                self.setGeometry(
                    self.geometry().x(),
                    self.geometry().y() + pos.y(),
                    self.width(),
                    self.height() - pos.y())
            if not (self.width() == self.minimumWidth() and pos.x() > 0):
                self.setGeometry(
                    self.geometry().x() + pos.x(),
                    self.geometry().y(),
                    self.width() - pos.x(),
                    self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()
    # endregion

    # region 音乐播放相关
    def _init_music_player(self):
        self.playlist = player.MusicStreamQueue('temp')
        self.q_player = player.MediaPlayer(myLyric, self)
        # self.q_player = player.MediaPlayer(None, self)

        self.timer = QTimer(self)
        self.timer.start(10)

        self.q_player.slider_reset_signal.connect(self.reset_slider_event)
        self.next_song_button.clicked.connect(self.q_player.next_song)
        self.last_song_button.clicked.connect(self.q_player.last_song)
        self.pause_button.clicked.connect(self.play_pause_player_event)
        self.progress_slider.sliderReleased.connect(self.slider_event)
        self.progress_slider.signal.connect(self.slider_event)
        self.timer.timeout.connect(self.timer_event)

    def reset_slider_event(self) -> None:
        time_text = self.q_player.playlist.now_song_info['duration'].split(':')
        duration = int(time_text[0]) * 60000 + int(time_text[1]) * 1000
        self.progress_slider.setMaximum(duration)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setValue(0)

    def play_pause_player_event(self) -> None:
        self.q_player.play_pause_player()
        self.progress_slider.setValue(self.q_player.position())

    def slider_event(self) -> None:
        self.q_player.set_position(self.progress_slider.value())

    def timer_event(self) -> None:
        if self.q_player.state() == 1:
            self.progress_slider.setValue(self.progress_slider.value() + 10)

    def load_play_list(self, playlist: player.MusicStreamQueue):
        self.playlist = deepcopy(playlist)
        self.q_player.load_playlist(self.playlist)
        self.reset_slider_event()
        self.play_pause_player_event()

    # endregion

    # region 歌词播放相关
    def _init_test(self):
        self.detail_stream_list_button.clicked.connect(self.test_event)

    def test_event(self):
        mode = random.randint(0, 2)
        if not self.q_player.lrc_play.set_trans_mode(mode):
            print("失败")
    # endregion



    def closeEvent(self, event) -> None:
        print('ui关闭')
        sys.exit(app.exec_())


class LeftListWidget(object):
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window

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

        self._init_base_item()

        self.main_window.left_sidebar_listwidget.itemClicked.connect(self.click_event)

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
            if inner_index == 2:
                self.main_window.stack_scrollarea.takeWidget()
                self.main_window.stack_scrollarea.setWidget(self.main_window.metadata_widget)

        elif index > self.download_api_item_index:
            pass

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

            self.item_num_play_list = len(os.listdir(player.PLAYLIST_SAVE_PATH))  # 获取歌单的数量
            for playlist_file in os.listdir(player.PLAYLIST_SAVE_PATH):
                pass  # todo 一次性创建playlist_widget

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


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myLyric = LyricsWindow()
    myWin = MainWindow()
    myWin.show()
    myLyric.show()
    sys.exit(app.exec_())

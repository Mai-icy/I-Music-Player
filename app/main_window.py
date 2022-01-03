#!/usr/bin/python
# -*- coding:utf-8 -*-
import random
import sys

from PIL import Image, ImageQt
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_source.MainWindow import Ui_MainWindow
import components.player as player
import common.song_metadata as sm

from components.lyrics_window.lyrics_window import LyricsWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint)
        self._init_music_player()
        self._init_signal_connect()

        self._init_test()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # 初始化无边框窗口拉伸拖动
        self.set_mouse_track()
        self._initDrag()
        self.installEventFilter(self)  # 初始化事件过滤器
        self.setMouseTracking(True)

    def _init_signal_connect(self):
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(self.showMinimized)  # 小化到任务栏

        self.left_sidebar_listwidget.play_music_signal.connect(self.load_play_list)
        self.left_sidebar_listwidget.kugou_api_widget.scroll2upSignal.connect(
            self.scroll_up_event)

        self.is_lyrics_checkbox.stateChanged.connect(self.is_lyrics_change_event)

    def is_lyrics_change_event(self):
        state = self.is_lyrics_checkbox.isChecked()
        if state:
            myLyric.setVisible(True)
        else:
            myLyric.setVisible(False)

    # region Widget相关事件连接

    # endregion

    def scroll_up_event(self):
        self.stack_scrollarea.ensureVisible(0, 0)

    # region 无边框窗口拉伸拖动相关
    def set_mouse_track(self):  # 设置鼠标跟踪
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.frame.setMouseTracking(True)
        self.below_bar_frame.setMouseTracking(True)
        # self.left_sidebar_listwidget.setMouseTracking(True)
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
        self._right_rect = [
            QPoint(
                x,
                y) for x in range(
                self.width() -
                5,
                self.width() +
                5) for y in range(
                5,
                self.height() -
                5)]
        self._bottom_rect = [
            QPoint(
                x,
                y) for x in range(
                5,
                self.width() -
                5) for y in range(
                self.height() -
                5,
                self.height() +
                5)]
        self._bottom_right_rect = [
            QPoint(
                x,
                y) for x in range(
                self.width() -
                5,
                self.width() +
                5) for y in range(
                self.height() -
                5,
                self.height() +
                5)]
        self._left_rect = [QPoint(x, y) for x in range(-5, 5)
                           for y in range(5, self.height() - 5)]
        self._upper_rect = [QPoint(x, y) for x in range(
            5, self.width() - 5) for y in range(-5, 5)]
        self._bottom_left_rect = [QPoint(x, y) for x in range(-5, 5) for y in
                                  range(self.height() - 5, self.height() + 5)]
        self._upper_right_rect = [QPoint(x, y) for x in range(
            self.width() - 5, self.width() + 5) for y in range(-5, 5)]
        self._upper_left_rect = [QPoint(x, y)
                                 for x in range(-5, 5) for y in range(-5, 5)]

    def mousePressEvent(self, event):  # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (
                event.pos() in self._bottom_right_rect):
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
            if not ((self.height() == self.minimumHeight() and pos.y() > 0) or (
                    self.height() == self.maximumHeight() and pos.y() < 0)):
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
            if not ((self.height() == self.minimumHeight() and pos.y() > 0) or (
                    self.height() == self.maximumHeight() and pos.y() < 0)):
                self.setGeometry(
                    self.geometry().x(),
                    self.geometry().y() + pos.y(),
                    pos.x(),
                    self.height() - pos.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._upper_left_drag:
            # 左上角同时调整高度和宽度
            if not ((self.height() == self.minimumHeight() and pos.y() > 0) or (
                    self.height() == self.maximumHeight() and pos.y() < 0)):
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
        self.q_player = player.MediaPlayer(myLyric, self)  # 是否生成歌词窗口
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
        self.song_title.setText(self.q_player.playlist.now_song_info["songName"])
        buffer = sm.get_album_buffer(self.q_player.playlist.now_song_info["songPath"])
        self.cover_pic_label.clear()
        self.cover_pic_label.setScaledContents(True)
        if buffer.getvalue():
            pic_data = Image.open(buffer)
            q_image = ImageQt.toqpixmap(pic_data)
            self.cover_pic_label.setPixmap(q_image)
            buffer.close()

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
        self.q_player.load_playlist(playlist)
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


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myLyric = LyricsWindow()
    myWin = MainWindow()
    myWin.show()
    myLyric.show()
    sys.exit(app.exec_())

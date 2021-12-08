# region imports
import sys
import time
from math import ceil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_source.LyricsWindow import Ui_LyricsWindow


class LyricsWindow(QWidget, Ui_LyricsWindow):
    def __init__(self, parent=None):
        super(LyricsWindow, self).__init__(parent)
        self.setupUi(self)
        self._init_main_window()  # 主窗口初始化设置
        self.installEventFilter(self)  # 初始化事件过滤器
        self._initDrag()
        self.set_button_hide(True)
        self.set_mouse_track()
        self.set_default_window_shadow()
        self._init_font()
        self._init_roll()

    # 字体初始化设置
    def _init_font(self):
        self.font = QtGui.QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPixelSize(int((self.height() - 30) / 5 * 4 / 2))
        self.text1_scrollarea.set_font(self.font)
        self.text2_scrollarea.set_font(self.font)

    # 主窗口初始化设置
    def _init_main_window(self):
        self.text1_scrollarea.set_text()
        self.text2_scrollarea.set_text()
        self.text1_scrollarea.set_label_stylesheet("color:rgb(86, 152, 195)")
        self.text2_scrollarea.set_label_stylesheet("color:rgb(86, 152, 195)")

    # 设置默认阴影
    def set_default_window_shadow(self):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # 偏移
        effect_shadow.setOffset(0, 0)
        # 阴影半径
        effect_shadow.setBlurRadius(10)
        # 阴影颜色
        effect_shadow.setColor(QtCore.Qt.gray)
        self.set_window_shadow(effect_shadow)

        # 设置窗口的阴影

    def set_window_shadow(self, shadow: QtWidgets.QGraphicsDropShadowEffect):

        self.background_frame.setGraphicsEffect(shadow)

        # 设置鼠标跟踪

    def set_mouse_track(self):
        self.setMouseTracking(True)
        self.background_frame.setMouseTracking(True)
        self.text1_scrollarea.set_mouse_track()
        self.text2_scrollarea.set_mouse_track()
        self.buttons_frame.setMouseTracking(True)

        # 定义鼠标移入事件,显示按钮,设置半透明背景

    def enterEvent(self, event):
        self.setStyleSheet("*\n"
                           "{\n"
                           "border:none;\n"
                           "}"
                           "#background_frame\n"
                           "{\n"
                           "    background-color: rgba(0,0,0,0.2);\n"
                           "}")
        self.set_button_hide(False)
        event.accept()

        # 定义鼠标移出事件,隐藏按钮,设置背景透明

    def leaveEvent(self, event):
        self.setStyleSheet("*\n"
                           "{\n"
                           "border:none;\n"
                           "}")
        self.set_button_hide(True)
        event.accept()

        # 隐藏按钮

    def set_button_hide(self, flag):
        self.close_button.setHidden(flag)
        self.last_button.setHidden(flag)
        self.lock_button.setHidden(flag)
        self.main_button.setHidden(flag)
        self.next_button.setHidden(flag)
        self.offsetDown_button.setHidden(flag)
        self.offsetUp_button.setHidden(flag)
        self.pause_button.setHidden(flag)
        self.settings_button.setHidden(flag)

        # 关闭程序

    def on_close_button_clicked(self):
        self.close()

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
        return super(LyricsWindow, self).eventFilter(obj, event)

        # 自定义窗口调整大小范围

    def resizeEvent(self, QResizeEvent):
        self._right_rect = [QPoint(x, y) for x in range(self.width() - 10, self.width() + 10) for y in
                            range(10, self.height() - 10)]
        self._bottom_rect = [
            QPoint(
                x,
                y) for x in range(
                10,
                self.width() -
                10) for y in range(
                self.height() -
                10,
                self.height() +
                10)]
        self._bottom_right_rect = [
            QPoint(
                x,
                y) for x in range(
                self.width() -
                10,
                self.width() +
                10) for y in range(
                self.height() -
                10,
                self.height() +
                10)]
        self._left_rect = [QPoint(x, y) for x in range(-10, 10)
                           for y in range(10, self.height() - 10)]
        self._upper_rect = [QPoint(x, y) for x in range(10, self.width() - 10)
                            for y in range(-10, 10)]
        self._bottom_left_rect = [QPoint(x,
                                         y) for x in range(-10,
                                                           10) for y in range(self.height() - 10,
                                                                              self.height() + 10)]
        self._upper_right_rect = [QPoint(x, y) for x in range(
            self.width() - 10, self.width() + 10) for y in range(-10, 10)]
        self._upper_left_rect = [QPoint(x, y) for x in range(-10, 10)
                                 for y in range(-10, 10)]

        # 重写鼠标点击的事件

    def mousePressEvent(self, event):
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
        elif (event.button() == Qt.LeftButton) and (10 < event.pos().x() < self.width() - 10
                                                    and 10 < event.pos().y() < self.height() - 10):
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    # 重写鼠标移动的事件
    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        # 判断鼠标位置切换鼠标手势
        if (pos in self._bottom_right_rect) or (
                pos in self._upper_left_rect):  # QMouseEvent.pos()获取相对位置
            self.text2_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
            self.buttons_frame.setCursor(
                QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif (pos in self._bottom_rect) or (pos in self._upper_rect):
            self.text2_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeVerCursor))
            self.buttons_frame.setCursor(
                QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif (pos in self._right_rect) or (pos in self._left_rect):
            self.text1_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeHorCursor))
            self.text2_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeHorCursor))
            self.buttons_frame.setCursor(
                QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif (pos in self._bottom_left_rect) or (pos in self._upper_right_rect):
            self.text2_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
            self.buttons_frame.setCursor(
                QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        else:
            self.text1_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            self.text2_scrollarea.set_cursor(
                QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            self.buttons_frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

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

        # 更改字体大小        
        self.font.setPixelSize((self.height() - 30) / 2 * 4 / 5)
        self.text1_scrollarea.set_font(self.font)
        self.text2_scrollarea.set_font(self.font)

        # 判断缩放后是否开启滚动并更改文本label大小
        self.text1_scrollarea.resize_label(self.get_text_width(self.text1_scrollarea.text))
        self.text2_scrollarea.resize_label(self.get_text_width(self.text2_scrollarea.text))

    # region 歌词滚动
    # 歌词滚动设置初始化
    def _init_roll(self):
        self.time_step = 20  # 刷新时间间隔
        self.move_step = 1  # 步长
        self.roll_time = 0
        self.roll_time_rate = 0.7
        self.begin_index = 0
        self.timer = QTimer()
        self.timer.setInterval(self.time_step)
        self.timer.timeout.connect(self.update_index)
        self.timer.start()

        # 计算文本的总宽度

    def get_text_width(self, text):
        song_font_metrics = QFontMetrics(self.font)
        return song_font_metrics.width(text)

        # 设置歌词文本

    def set_text(self, rows, text, roll_time):
        width = self.get_text_width(text)
        self.roll_time = roll_time
        if rows == 1:
            self.text1_scrollarea.set_text(text, width)
        if rows == 2:
            self.text2_scrollarea.set_text(text, width)

        def get_move_step(width_t):
            if not roll_time:
                return 0
            return ceil(2 * (self.time_step * (width_t - self.width())) / (roll_time * self.roll_time_rate))

        if self.text1_scrollarea.text_width > self.text2_scrollarea.text_width:
            self.move_step = get_move_step(self.text1_scrollarea.text_width)
        else:
            self.move_step = get_move_step(self.text2_scrollarea.text_width)
        self.begin_index = (0.5 * (1 - self.roll_time_rate) * self.roll_time) // self.time_step

    def update_index(self):
        self.text1_scrollarea.update_index(self.begin_index, self.move_step)
        self.text2_scrollarea.update_index(self.begin_index, self.move_step)
# endregion


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = LyricsWindow()
    myWin.set_text(1, 'test', 1)
    myWin.set_text(2, 'test', 1)
    myWin.show()
    sys.exit(app.exec_())

import sys
import time
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_source.PlayListWidget import Ui_PlayListWidget


class PlayListWidget(QWidget, Ui_PlayListWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)
        # self.song_data_tablewidget.setMinimumSize(SongTableWidget.get_table_widget_size(self.song_data_tablewidget))
        self.setMinimumSize(self.get_table_widget_size(self.song_data_tablewidget))  # 设置最小值
        # self.song_data_tablewidget.setColumnWidth(0, 200)  # 设置指定列宽

    def resize_widget(self):
        self.setMinimumSize(self.get_table_widget_size(self.song_data_tablewidget))

    @staticmethod
    def get_table_widget_size(table):
        w = table.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(table.columnCount()):
            w += table.columnWidth(i)
        h = table.horizontalHeader().height() + 4
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        h += 238  # 添加了表格上面控件的长度

        return QtCore.QSize(w, h)


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = PlayListWidget()
    myWin.show()
    sys.exit(app.exec_())

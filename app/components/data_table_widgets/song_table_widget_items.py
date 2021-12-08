# encoding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_source.SongTableWidgetItem import Ui_SongTableWidgetItem


class SongTableWidgetItems(QWidget, Ui_SongTableWidgetItem):
    enterSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SongTableWidgetItems, self).__init__(parent)
        self.setupUi(self)
        self.play_button.setVisible(False)
        self.other_button.setVisible(False)
        self.append2next_button.setVisible(False)
        self.setMouseTracking(True)

    def enterEvent(self, a0: QEvent) -> None:
        self.enterSignal.emit('')


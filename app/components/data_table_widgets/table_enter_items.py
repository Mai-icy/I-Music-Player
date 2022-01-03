# encoding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_source.SongTableWidgetItem import Ui_SongTableWidgetItem


class SongTableWidgetItems(QWidget, Ui_SongTableWidgetItem):
    enterSignal = pyqtSignal(str)
    renameSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SongTableWidgetItems, self).__init__(parent)
        self.setupUi(self)
        self.play_button.setVisible(False)
        self.other_button.setVisible(False)
        self.append2next_button.setVisible(False)
        self.setMouseTracking(True)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        action_rename = menu.addAction('重命名')
        action_rename.triggered.connect(self.rename_event)
        action_remove = menu.addAction('删除')
        action_remove.triggered.connect(self.remove_event)
        action_remove = menu.addAction('属性')
        action_remove.triggered.connect(self.attributes_event)
        menu.exec_(QCursor.pos())

    def rename_event(self):
        self.rename_signal.emit(self.item_text)

    def remove_event(self):
        self.remove_signal.emit(self.item_text)

    def attributes_event(self):
        pass

    def enterEvent(self, a0: QEvent) -> None:
        self.enterSignal.emit('')

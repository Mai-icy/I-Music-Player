#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_source.dialog_box.NewPlaylistDialog import Ui_SingleInputDialog


class SingleInputDialog(QDialog, Ui_SingleInputDialog):
    done_signal = pyqtSignal(str)

    def __init__(self, parent, title_text, edit_text=""):
        super(SingleInputDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.lineEdit.setPlaceholderText(edit_text)
        self.label.setText(title_text)
        self._init_signal()

    def _init_signal(self):
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.done_event)

    def done_event(self):
        self.done_signal.emit(self.lineEdit.text())
        self.accept()

    def closeEvent(self, QCloseEvent):
        super(SingleInputDialog, self).closeEvent(QCloseEvent)
        self.done_signal.emit('')

    def reject(self):
        super(SingleInputDialog, self).reject()
        self.done_signal.emit('')


if __name__ == "__main__":
    # 适配2k等高分辨率屏幕,低分辨率屏幕可以缺省
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myLyric = SingleInputDialog(None, "?")
    myLyric.show()
    sys.exit(app.exec_())

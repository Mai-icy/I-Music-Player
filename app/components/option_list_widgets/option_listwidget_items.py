#!/usr/bin/python
# -*- coding:utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PlaylistItemsWidget(QWidget):
    def __init__(self, text):
        super(PlaylistItemsWidget, self).__init__()
        self.text = text
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(215, 39)
        Form.setMinimumSize(QSize(0, 30))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QPushButton(Form)
        self.pushButton.setMinimumSize(QSize(20, 20))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setMinimumSize(QSize(20, 20))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", self.text))


class PlaylistItemWidget(QWidget):
    rename_signal = pyqtSignal(str)
    remove_signal = pyqtSignal(str)

    def __init__(self, item_text: str, parent=None):
        self.item_text = item_text
        super(PlaylistItemWidget, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        action_rename = menu.addAction('重命名')
        action_rename.triggered.connect(self.rename_event)
        action_remove = menu.addAction('删除')
        action_remove.triggered.connect(self.remove_event)
        menu.exec_(QCursor.pos())

    def rename_event(self):
        self.rename_signal.emit(self.item_text)

    def remove_event(self):
        self.remove_signal.emit(self.item_text)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TableWidgetItem.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SongTableWidgetItem(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(453, 76)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(18, 11, 8, 11)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.is_like_checkbox = QtWidgets.QCheckBox(Form)
        self.is_like_checkbox.setText("")
        self.is_like_checkbox.setObjectName("is_like_checkbox")
        self.horizontalLayout_2.addWidget(self.is_like_checkbox)
        self.song_name_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.song_name_label.setFont(font)
        self.song_name_label.setObjectName("song_name_label")
        self.horizontalLayout_2.addWidget(self.song_name_label)
        spacerItem = QtWidgets.QSpacerItem(247, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.play_button = QtWidgets.QPushButton(Form)
        self.play_button.setText("")
        self.play_button.setObjectName("play_button")
        self.horizontalLayout.addWidget(self.play_button)
        self.append2next_button = QtWidgets.QPushButton(Form)
        self.append2next_button.setText("")
        self.append2next_button.setObjectName("append2next_button")
        self.horizontalLayout.addWidget(self.append2next_button)
        self.other_button = QtWidgets.QPushButton(Form)
        self.other_button.setText("")
        self.other_button.setObjectName("other_button")
        self.horizontalLayout.addWidget(self.other_button)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.song_name_label.setText(_translate("Form", "123"))

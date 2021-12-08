# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from components.progress_sliders import ProgressSlider

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1020, 700))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.title_label = QtWidgets.QLabel(self.frame)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout_2.addWidget(self.title_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mini_mode_button = QtWidgets.QPushButton(self.frame)
        self.mini_mode_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mini_mode_button.setMouseTracking(False)
        self.mini_mode_button.setText("")
        self.mini_mode_button.setCheckable(False)
        self.mini_mode_button.setAutoDefault(False)
        self.mini_mode_button.setDefault(False)
        self.mini_mode_button.setObjectName("mini_mode_button")
        self.horizontalLayout.addWidget(self.mini_mode_button)
        self.minimize_button = QtWidgets.QPushButton(self.frame)
        self.minimize_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minimize_button.setText("")
        self.minimize_button.setObjectName("minimize_button")
        self.horizontalLayout.addWidget(self.minimize_button)
        self.maximize_button = QtWidgets.QPushButton(self.frame)
        self.maximize_button.setBaseSize(QtCore.QSize(0, 0))
        self.maximize_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.maximize_button.setText("")
        self.maximize_button.setObjectName("maximize_button")
        self.horizontalLayout.addWidget(self.maximize_button)
        self.close_button = QtWidgets.QPushButton(self.frame)
        self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.setText("")
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.left_sidebar_listwidget = QtWidgets.QListWidget(self.centralwidget)
        self.left_sidebar_listwidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.left_sidebar_listwidget.setObjectName("left_sidebar_listwidget")
        self.horizontalLayout_3.addWidget(self.left_sidebar_listwidget)
        self.stack_scrollarea = QtWidgets.QScrollArea(self.centralwidget)
        self.stack_scrollarea.setWidgetResizable(True)
        self.stack_scrollarea.setObjectName("stack_scrollarea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 812, 523))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.stack_scrollarea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.stack_scrollarea)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.below_bar_frame = QtWidgets.QFrame(self.centralwidget)
        self.below_bar_frame.setMinimumSize(QtCore.QSize(0, 69))
        self.below_bar_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.below_bar_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.below_bar_frame.setObjectName("below_bar_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.below_bar_frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.progress_slider = ProgressSlider(self.below_bar_frame)
        self.progress_slider.setOrientation(QtCore.Qt.Horizontal)
        self.progress_slider.setObjectName("progress_slider")

        self.verticalLayout_4.addWidget(self.progress_slider)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(13)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cover_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.cover_button.setMinimumSize(QtCore.QSize(50, 50))
        self.cover_button.setText("")
        self.cover_button.setObjectName("cover_button")
        self.horizontalLayout_8.addWidget(self.cover_button)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.song_title = QtWidgets.QLabel(self.below_bar_frame)
        self.song_title.setMinimumSize(QtCore.QSize(130, 0))
        self.song_title.setObjectName("song_title")
        self.verticalLayout_3.addWidget(self.song_title)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.is_like_checkBox = QtWidgets.QCheckBox(self.below_bar_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.is_like_checkBox.sizePolicy().hasHeightForWidth())
        self.is_like_checkBox.setSizePolicy(sizePolicy)
        self.is_like_checkBox.setMinimumSize(QtCore.QSize(25, 25))
        self.is_like_checkBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.is_like_checkBox.setBaseSize(QtCore.QSize(0, 0))
        self.is_like_checkBox.setText("")
        self.is_like_checkBox.setIconSize(QtCore.QSize(16, 16))
        self.is_like_checkBox.setAutoRepeatDelay(300)
        self.is_like_checkBox.setObjectName("is_like_checkBox")
        self.horizontalLayout_7.addWidget(self.is_like_checkBox)
        self.more_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.more_button.setMinimumSize(QtCore.QSize(25, 25))
        self.more_button.setText("")
        self.more_button.setObjectName("more_button")
        self.horizontalLayout_7.addWidget(self.more_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.last_song_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.last_song_button.setMinimumSize(QtCore.QSize(40, 40))
        self.last_song_button.setText("")
        self.last_song_button.setObjectName("last_song_button")
        self.horizontalLayout_6.addWidget(self.last_song_button)
        self.pause_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.pause_button.setMinimumSize(QtCore.QSize(40, 40))
        self.pause_button.setText("")
        self.pause_button.setObjectName("pause_button")
        self.horizontalLayout_6.addWidget(self.pause_button)
        self.next_song_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.next_song_button.setMinimumSize(QtCore.QSize(40, 40))
        self.next_song_button.setText("")
        self.next_song_button.setObjectName("next_song_button")
        self.horizontalLayout_6.addWidget(self.next_song_button)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.progress_labe = QtWidgets.QLabel(self.below_bar_frame)
        self.progress_labe.setMinimumSize(QtCore.QSize(71, 0))
        self.progress_labe.setObjectName("progress_labe")
        self.horizontalLayout_5.addWidget(self.progress_labe)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.volume_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.volume_button.setMinimumSize(QtCore.QSize(25, 25))
        self.volume_button.setText("")
        self.volume_button.setObjectName("volume_button")
        self.horizontalLayout_4.addWidget(self.volume_button)
        self.stream_mode_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.stream_mode_button.setText("")
        self.stream_mode_button.setObjectName("stream_mode_button")
        self.horizontalLayout_4.addWidget(self.stream_mode_button)
        self.is_lyrics_checkbox = QtWidgets.QCheckBox(self.below_bar_frame)
        self.is_lyrics_checkbox.setText("")
        self.is_lyrics_checkbox.setObjectName("is_lyrics_checkbox")
        self.horizontalLayout_4.addWidget(self.is_lyrics_checkbox)
        self.detail_stream_list_button = QtWidgets.QPushButton(self.below_bar_frame)
        self.detail_stream_list_button.setText("")
        self.detail_stream_list_button.setObjectName("detail_stream_list_button")
        self.horizontalLayout_4.addWidget(self.detail_stream_list_button)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.below_bar_frame)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate("MainWindow", "TextLabel"))
        self.song_title.setText(_translate("MainWindow", "TextLabel"))
        self.progress_labe.setText(_translate("MainWindow", "00:00"))

# coding:utf-8

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ProgressSlider(QSlider):  # 使进度条指哪里点哪里 重写mousePressEvent事件
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        # super(MySlider, self).__init__(parent)
        super(ProgressSlider, self).__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setSingleStep(1)

        '''
        self.m_displayLabel = QLabel()
        self.m_displayLabel.setFixedSize(QSize(20, 20))
        #  设置游标背景为白色
        self.m_displayLabel.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.m_displayLabel.setPalette(palette)

        self.m_displayLabel.setAlignment(Qt.AlignCenter)

        self.m_displayLabel.setVisible(False)
        self.m_displayLabel.move(0, 3)'''

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mousePressEvent(event)  # 调用父级的单击事件，听说这样能不影响进度条原来的拖动
            val_por = event.pos().x() / self.width()  # 获取鼠标在进度条的相对位置
            self.setValue(int(val_por * self.maximum()))  # 改变进度条的值
            self.signal.emit('')  # 点击发送信号，这里可不要
            '''
        if not self.m_displayLabel.isVisible():
            self.m_displayLabel.setVisible(True)
            self.m_displayLabel.setText(str(self.value()))

    def mouseReleaseEvent(self, event):
        if self.m_displayLabel.isVisible():
            self.m_displayLabel.setVisible(False)

    def mouseMoveEvent(self, event):
        self.m_displayLabel.setText(str(self.value()))
        self.m_displayLabel.move(int((self.width() -
                                      self.m_displayLabel.width()) *
                                 self.value() /
                                 (self.maximum() -
                                  self.minimum())), 3)
        '''






# encoding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from components.player.music_stream_queue import MusicStreamQueue
from components.data_table_widgets.song_table_widget_items import SongTableWidgetItems


class SongTableWidget(QTableWidget):
    double_click_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(SongTableWidget, self).__init__(parent)
        self.last_item = None
        self._init_content()
        self._init_base_config()
        self._init_mouse_track()
        """
        self.setStyleSheet('''
        QTableView
        {
            background: rgb(55,55,55);
        }
        QTableView{
            selection-background-color:rgb(255,0,0);
            background-color:rgb(50,50,50);
            border:1px solid rgb(70,70,70);
            color:rgb(200,200,200)
        }
        
        QTableView::item
        {
               border:1px solid rgb(65,65,65);
            color:rgb(200,200,200);
        
        }
        QTableView::item:hover
        {
            background-color: rgb(30,30,30);
            font: 75 9pt "Microsoft YaHei";
            color:rgb(31,163,246);
        }
        QTableView::item::selected
        {
            background-color: rgb(30,30,30);
            font: 75 9pt "Microsoft YaHei";
            color:rgb(31,163,246);
        }
        
        
        
        
        QHeaderView::section{
            background-color:rgb(90,90,90);
              color:rgb(200,200,200);
            border:1px solid rgb(60,60,60);
            border-bottom:1px solid rgb(70,70,70);
            height:27px;
            min-width:55px;
        }
        QHeaderView::section:hover
        {
            background-color:rgb(80,80,80);
        
        }
        ''')
        """

    # region 初始化函数
    def _init_mouse_track(self):
        self.setMouseTracking(True)
        # self.parent().setMouseTracking(True)
        self.is_enter_event = True

    def _init_base_config(self):  # 基本表格默认参数设置
        self.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContentsOnFirstShow)

        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setSortIndicatorShown(False)
        self.horizontalHeader().setStretchLastSection(False)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(47)
        self.horizontalHeader().setMinimumHeight(30)  # 表头高度

        # 设置让表示歌曲名的一列自动延伸
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        # self.setColumnWidth(0, 380)  # 设置指定列宽
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 180)
        self.setColumnWidth(3, 100)

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(True)  # 允许拖拽操作，并在之后重写事件
        self.setAcceptDrops(True)
        self.verticalHeader().setVisible(False)
        self.setDropIndicatorShown(True)
        self.setShowGrid(False)

    def _init_content(self):
        self.setColumnCount(4)
        self.setRowCount(0)

        column_text_list = ['歌曲名', '歌手', '专辑', '时长']
        for column in range(0, 4):
            item = QTableWidgetItem()
            item.setText(column_text_list[column])
            self.setHorizontalHeaderItem(column, item)
        '''
        for row in range(0, 20):
            item = QTableWidgetItem()
            self.setVerticalHeaderItem(0, item)
        '''

    # endregion

    # region 重写事件

    def enterEvent(self, a0: QEvent = None) -> None:
        # todo 鼠标追踪失效
        if self.is_enter_event:
            point = self.mapFromGlobal(self.cursor().pos())  # 转换为相对位置
            point.setY(point.y() - 31)  # 表头的高度+1（表头的高度为30
            # point = self.cursor().pos()
            # point.setX(point.x() - 690)
            # point.setY(point.y() - 520)
            point.setX(10)
            item = self.itemAt(point)
            if item:
                if item != self.last_item:
                    if self.last_item:
                        try:
                            widget_item = self.cellWidget(
                                self.last_item.row(), 0)

                            widget_item.play_button.setVisible(False)
                            widget_item.other_button.setVisible(False)
                            widget_item.append2next_button.setVisible(False)
                        except RuntimeError:  # qt抛出错误，在拖拽操作时引发
                            pass
                        except AttributeError:
                            pass
                    self.last_item = item
                widget_item = self.cellWidget(item.row(), 0)
                widget_item.play_button.setVisible(True)
                widget_item.other_button.setVisible(True)
                widget_item.append2next_button.setVisible(True)

    def dropEvent(self, event):
        qDebug("dropEvent")
        row_src = self.currentRow()
        pos = event.pos()
        # 使选点pos，获取的落点item在有文字的cell内部，防止因为none触发问题
        pos.setX(self.width() - 150)
        item = self.itemAt(pos)  # 获取落点的item
        if item.row() == row_src:
            return
        if item:
            self.playlist.adjust_position(row_src, item.row())

            row_dst = item.row()
            if row_src > row_dst:
                row_src += 1
            if row_src < row_dst:
                row_dst += 1
            self.insertRow(row_dst)

        else:
            row_dst = self.rowCount()
            self.insertRow(row_dst)

        # 对拖动后位置的第一个单元格进行重新配布
        item = QTableWidgetItem()
        item.setText(' ')
        widget_item = self.cellWidget(row_src, 0)
        song_name = widget_item.song_name_label.text()
        widget_item = SongTableWidgetItems()
        widget_item.song_name_label.setText(song_name)
        widget_item.enterSignal.connect(self.enterEvent)
        self.setItem(row_dst, 0, item)
        self.setCellWidget(row_dst, 0, widget_item)
        # 配布完毕，下面的i不经历0

        for i in range(1, self.columnCount()):
            self.setItem(row_dst, i, self.takeItem(row_src, i))

        self.selectRow(row_dst)  # 选中移动后的项
        self.removeRow(row_src)

    def leaveEvent(self, *args, **kwargs):  # 当鼠标离开表格，隐藏按钮
        if self.last_item:
            try:
                widget_item = self.cellWidget(self.last_item.row(), 0)
                widget_item.play_button.setVisible(False)
                widget_item.other_button.setVisible(False)
                widget_item.append2next_button.setVisible(False)
            except RuntimeError:  # qt抛出错误，在拖拽操作时引发
                pass
            except AttributeError:
                pass

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            pos = e.pos()
            # 使选点pos，获取的落点item在有文字的cell内部，防止因为none触发问题
            pos.setX(self.width() - 150)
            select_row = self.itemAt(pos).row()
            # print(self.playlist.music_stream_list[select_row])
            self.double_click_signal.emit(select_row)
            # todo 选中返回对应列

    # endregion

    # 其他功能连接提供
    def load_playlist(self, playlist: MusicStreamQueue):
        self.clearContents()
        self.setRowCount(len(playlist.playlist["songInfo_list"]))

        self.playlist = playlist

        for music_index in range(0, len(playlist.playlist["songInfo_list"])):
            music_info = playlist.playlist["songInfo_list"][music_index]

            item = QTableWidgetItem()
            widget_item = SongTableWidgetItems()
            widget_item.song_name_label.setText(music_info['songName'])
            item.setText(' ')
            widget_item.enterSignal.connect(
                self.enterEvent)  # 使用widget的信号连接鼠标检测事件
            self.setItem(music_index, 0, item)
            self.setCellWidget(music_index, 0, widget_item)

            item = QTableWidgetItem()
            item.setText(music_info['singer'])
            self.setItem(music_index, 1, item)

            item = QTableWidgetItem()
            item.setText(music_info['album'])
            self.setItem(music_index, 2, item)

            item = QTableWidgetItem()
            item.setText(music_info['duration'])
            self.setItem(music_index, 3, item)


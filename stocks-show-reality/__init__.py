import sys
import efinance as ef
import time
import requests
import pandas
import tkinter as tk
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QShortcut, QMenu
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence
from PyQt5.QtCore import Qt, QTimer, QObject, QEvent
import web3_calculator

class TooltipWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.ToolTip)
        self.data = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.data)
        self.setLayout(layout)


class BallWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(10, 1180, 100, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._drag_position = None
        self.tooltipWidget = TooltipWidget()

        # Set up a timer to refresh the data
        self.timer = QTimer(self)
        # self.timer.setInterval(1000)  # Update every second
        self.timer.setInterval(5000)  # Update every second
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

        # control visible
        # self.is_tooltipvisible = True
        # self.is_tooltipvisible = False

        self.hotkey_enabled = True  # Add a flag to control hotkey functionality
        self.hotkey_cooldown_ms = 500  # Cooldown time in milliseconds

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        show = menu.addAction("Show")
        hide = menu.addAction("Hide")

        action = menu.exec_(self.mapToGlobal(event.pos()))
        # print(action)
        if action == show:
            self.tooltipWidget.move(
                self.pos().x(), self.pos().y() - self.tooltipWidget.height())
            self.tooltipWidget.show()
        elif action == hide:
            self.tooltipWidget.hide()

    def toggle_widget(self):
        if not self.hotkey_enabled:
            return  # If hotkey is disabled, do nothing
        self.hotkey_enabled = False  # Disable hotkey functionality temporarily
        QTimer.singleShot(self.hotkey_cooldown_ms, lambda: setattr(self, "hotkey_enabled", True))  # Re-enable hotkey after cooldown
        if self.isHidden():
            self.show()
        else:
            self.hide()

    # def toggle_widget(self):
    #     print('toggle')
    #     if self.isHidden():
    #         self.show()
    #     else:
    #         self.hide()

    # def toggle_tooltip(self):
    #     if self.is_tooltipvisible:
    #         self.is_tooltipvisible = not self.is_tooltipvisible
    #         self.tooltipWidget.hide()
    #     else:
    #         self.is_tooltipvisible = not self.is_tooltipvisible
    #         self.tooltipWidget.move(
    #             self.pos().x(), self.pos().y() - self.tooltipWidget.height())
    #         self.tooltipWidget.show()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(QColor(104, 108, 117))
        qp.drawEllipse(10, 10, 40, 40)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # print('mouseMoveEvent')
        if event.buttons() == Qt.LeftButton and self._drag_position:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # print('mouseReleaseEvent')
        if event.button() == Qt.LeftButton:
            self._drag_position = None

    def enterEvent(self, event):
        # self.update_data()
        # print('enterEvent')
        self.tooltipWidget.move(
            self.pos().x(), self.pos().y() - self.tooltipWidget.height())
        self.tooltipWidget.show()

    def leaveEvent(self, event):
        # print('leaveEvent')
        self.tooltipWidget.hide()

    def update_data(self):
        # 如果在监控时间内
        if is_control():
          # {"sz001300": "sb", "sz002786": "yb", "sh603825": ""}
          given = ['002189', '002395', '603628', '600630', '002786', '002127', '002771', '600178', '001300']
          # TODO: 1.调用接口，获取到实时的数据（高频、快速）
          stock_infos = ef.stock.get_realtime_quotes()
          # TODO: 2.组装返回的结果，格式为：stock_name, alias。如果alisa为空字符串，
          filtered_given = stock_infos[stock_infos['股票代码'].isin(given)]
          data_text = ''
          for row in filtered_given.itertuples():
            data_text += row[2] + ' now:' + str(row[4]) + ' inc:' + str(row[3]) + '\n'
        #   print(data_text)
        # 如果不在监控时间内
        else:
          data_text = 'not in control time'
          print('not in control time')
        self.tooltipWidget.data.setText(data_text)
        self.tooltipWidget.adjustSize()


def is_control():
    """
      是否在 09:15:00 - 15:00:00

      Returns
      -------
      bool
    """
    st = '09:15:00'
    # et = '15:00:00'
    et = '15:30:00'
    dt = datetime.now()
    return st <= dt.strftime('%H:%M:%S') <= et

if __name__ == '__main__':
    time.sleep(1)
    # pyinstaller -F -c __init__.py
    # cd ..
    # python setup.py sdist bdist_wheel
    # twine upload dist/*
    # __token__
    # pypi-AgEIcHlw
    app = QApplication(sys.argv)
    ex = BallWidget()

    ex.show()
    sys.exit(app.exec_())

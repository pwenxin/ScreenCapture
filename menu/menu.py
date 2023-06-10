import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QAction

from setting import mwidth, mheight, set_screen_num, get_screen_num

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建菜单栏
        menu_bar = self.menuBar()
        # 创建“文件”菜单
        file_menu = menu_bar.addMenu('设置')
        # 添加“新建”操作到“文件”菜单
        new_action = QAction('切屏', self)
        file_menu.addAction(new_action)
        new_action.triggered.connect(self.new_file)
        self.setGeometry(100, 100, mwidth, mheight)
        self.setWindowTitle('ScreenCapture')

    def new_file(self):
        num = (get_screen_num() + 1) % len(QGuiApplication.screens())
        set_screen_num(num)

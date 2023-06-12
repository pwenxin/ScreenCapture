import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QAction
from PyQt5.QtGui import QPixmap, QGuiApplication, QCursor
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtCore import QSize
from menu.menu import Menu
from setting import mwidth, mheight, get_screen_num


class ScreenCapture(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, mwidth, mheight)
        self.setWindowTitle('Screen Capture')

        # get the geometry of the specified screen
        screen = QGuiApplication.screens()[get_screen_num()]
        self.screen_geometry = screen.geometry()

        # create a label to display the captured screen
        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.label.setAlignment(Qt.AlignCenter)

        self.cursor_label = QLabel(self)
        scaled_pixmap = QPixmap('cursor.png').scaled(QSize(15, 15))
        self.cursor_label.setPixmap(scaled_pixmap)
        self.cursor_label.setWindowFlag(Qt.WindowStaysOnTopHint)

        # create a timer to periodically capture the screen and update the widget
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateScreen)
        self.timer.start(100)  # update the screen every 100 milliseconds

    def updateScreen(self):
        # capture the screen and display it on the label
        screen = QGuiApplication.screens()[get_screen_num()]
        screen_pixmap = screen.grabWindow(0)
        self.label.setGeometry(0, 0, QGuiApplication.topLevelWindows()[0].geometry().width(),
                               QGuiApplication.topLevelWindows()[0].geometry().height())
        self.label.setPixmap(screen_pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # get the current mouse position relative to the widget and update the QPoint attribute
        mouse_pos = QCursor.pos()
        geometry = screen.geometry()
        self.cursor_label.move(
            int((mouse_pos.x() - geometry.x()) / geometry.width() * QGuiApplication.topLevelWindows()[0].geometry().width()),
            int((mouse_pos.y() - geometry.y()) / geometry.height() * QGuiApplication.topLevelWindows()[0].geometry().height()))
        self.update()

    def keyPressEvent(self, event):
        # exit the program when the Esc key is pressed
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Menu()
    screen_capture = ScreenCapture()
    window.setCentralWidget(screen_capture)

    window.show()
    sys.exit(app.exec_())

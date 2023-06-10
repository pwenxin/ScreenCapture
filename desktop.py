import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication, QCursor, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
from PyQt5.QtCore import QSize

class ScreenCapture(QWidget):
    def __init__(self, screen_num):
        self.mwidth = 960
        self.mheight = 540
        super().__init__()
        self.screen_num = screen_num
         # add a QPoint attribute to store the mouse position
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, self.mwidth, self.mheight)
        self.setWindowTitle('Screen Capture')

        # get the geometry of the specified screen
        screen = QGuiApplication.screens()[self.screen_num]
        self.screen_geometry = screen.geometry()

        # create a label to display the captured screen
        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.label.setAlignment(Qt.AlignCenter)

        self.cursor_label = QLabel(self)
        # self.cursor_label.setGeometry(QRect(0, 0, 5, 5))
        # self.cursor_label.setStyleSheet('background-color: #000000')
        scaled_pixmap = QPixmap('cursor.png').scaled(QSize(15, 15))
        self.cursor_label.setPixmap(scaled_pixmap)
        self.cursor_label.setWindowFlag(Qt.WindowStaysOnTopHint)
        # self.cursor_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # create a timer to periodically capture the screen and update the widget
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateScreen)
        self.timer.start(30)  # update the screen every 100 milliseconds

    def updateScreen(self):
        # capture the screen and display it on the label
        screen = QGuiApplication.screens()[self.screen_num]
        screen_pixmap = screen.grabWindow(0)
        self.label.setPixmap(screen_pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # get the current mouse position relative to the widget and update the QPoint attribute
        mouse_pos = QCursor.pos()
        geometry = screen.geometry()
        self.cursor_label.move(int((mouse_pos.x() - geometry.x())/geometry.width()*self.mwidth),int((mouse_pos.y() - geometry.y())/geometry.height()*self.mheight))
        self.update()


    def keyPressEvent(self, event):
        # exit the program when the Esc key is pressed
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_num = 0  # specify the screen number to capture, starting from 0
    screen_capture = ScreenCapture(screen_num)
    screen_capture.show()
    sys.exit(app.exec_())

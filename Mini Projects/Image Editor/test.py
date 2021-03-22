import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# from PyQt4 import QtCore, QtWidgets

class ResizableRubberBand(QWidget):
    def __init__(self, parent=None):
        super(ResizableRubberBand, self).__init__(parent)

        self.draggable = True
        self.dragging_threshold = 1
        self.mousePressPos = None
        self.mouseMovePos = None
        self.borderRadius = 0

        self.setWindowFlags(Qt.SubWindow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignTop)

        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignBottom | Qt.AlignLeft)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignBottom | Qt.AlignRight)
        self._band = QtWidgets.QRubberBand(QRubberBand.Rectangle, self)

        self._band.show()
        self.show()

    def resizeEvent(self, event):
        self._band.resize(self.size())

    def paintEvent(self, event):
        # Get current window size
        window_size = self.size()

        qp = QPainter(self)
        # print(11)
        # qp.begin(self)
        #qp.setRenderHint(QtWidgets.QPainter.Antialiasing, True)
        qp.drawRoundedRect(0, 0, window_size.width(), window_size.height(), self.borderRadius, self.borderRadius)
        #qp.end()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == QtCore.Qt.RightButton:
            self.mousePressPos = event.globalPos()  # global
            self.mouseMovePos = event.globalPos() - self.pos()  # local
            print(self.pos())
        #super(ResizableRubberBand, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & QtCore.Qt.RightButton:
            globalPos = event.globalPos()
            #print(globalPos)
            moved = globalPos - self.mousePressPos
            print(moved)
            if moved.manhattanLength() > self.dragging_threshold:
                # Move when user drag window more than dragging_threshold
                diff = globalPos - self.mouseMovePos
                self.move(diff)
                self.mouseMovePos = globalPos - self.pos()
        #super(ResizableRubberBand, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            if event.button() == QtCore.Qt.RightButton:
                moved = event.globalPos() - self.mousePressPos
                # if moved.manhattanLength() > self.dragging_threshold:
                #     # Do not call click event or so on
                #
                #     event.ignore()
                self.mousePressPos = None
        #super(ResizableRubberBand, self).mouseReleaseEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QtWidgets.QPushButton('Show Rubber Band')
        self.button.clicked.connect(self.handleButton)
        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap('image.JPG'))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def handleButton(self):
        self.band = ResizableRubberBand(self.label)
        self.band.setGeometry(150, 150, 150, 150)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(800, 100, 600, 500)
    window.show()
    sys.exit(app.exec_())

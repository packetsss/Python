import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        self.create_graphic_view()

    def create_graphic_view(self):
        self.scene = QGraphicsScene()
        self.greenbrush = QBrush(Qt.green)
        self.graybrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0, 0, 800, 600)

        self.shapes()

    def shapes(self):
        elps = self.scene.addEllipse(20, 20, 200, 200, self.pen, self.greenbrush)
        rect = self.scene.addRect(-100, -100, 200, 200, self.pen, self.graybrush)

        elps.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        elps.setFlag(QGraphicsItem.ItemIsSelectable)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

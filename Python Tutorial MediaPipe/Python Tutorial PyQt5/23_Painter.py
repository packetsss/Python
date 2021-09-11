# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 800, 400)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        # change to config

        painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))
        # or solid pattern

        painter.drawRect(100, 15, 300, 100)

        ellipse = QPainter(self)
        ellipse.setPen(QPen(Qt.black, 4, Qt.DashDotDotLine))
        ellipse.setBrush(QBrush(Qt.yellow, Qt.Dense2Pattern))
        # Dense, Pattern is transparency

        ellipse.drawEllipse(100, 150, 400, 200)

        text = QPainter(self)
        text.drawText(100, 100, "Hi!")
        rect = QRect(100, 150, 250, 250)

        text.drawRect(rect)
        text.drawText(rect, Qt.AlignCenter, "OOf")
        # draw text in rect

        document = QTextDocument()
        rect2 = QRectF(0, 0, 250, 250)
        document.setTextWidth(rect2.width())
        document.setHtml("<b>OOf llo</b> <i> Dev </i> <font size = '12' color='green>I love you.com </font>")
        document.drawContents(painter, rect2)

        polygon = QPolygon([QPoint(10, 10), QPoint(20, 120), QPoint(120, 60), QPoint(100, 100)])
        painter.drawPolygon(polygon)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

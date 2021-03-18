import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        vbox = QVBoxLayout()
        btn1 = QPushButton("Click 1")
        btn2 = QPushButton("Click 2")
        btn3 = QPushButton("Click 3")
        btn4 = QPushButton("Click 4")

        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        # add btns to the vbox layout

        self.setLayout(vbox)
        # aligned vertically


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

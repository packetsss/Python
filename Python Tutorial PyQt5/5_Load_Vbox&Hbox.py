from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt5 import uic
import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\Vbox_layouts.ui", self)
        # can also edit the ui file

        hbox = QHBoxLayout()
        btn1 = QPushButton("Click 1")
        btn2 = QPushButton("Click 2")
        btn3 = QPushButton("Click 3")
        btn4 = QPushButton("Click 4")

        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        hbox.addWidget(btn4)

        self.setLayout(hbox)


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()
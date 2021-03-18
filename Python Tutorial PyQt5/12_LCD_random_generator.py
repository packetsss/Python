import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, \
    QRadioButton, QDialog, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, QTime, QTimer
from random import randint


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        vbox = QVBoxLayout()

        self.lcd = QLCDNumber()

        # self.lcd.setStyleSheet("background-color:pink")
        self.lcd.setStyleSheet("color:pink")

        vbox.addWidget(self.lcd)

        btn = QPushButton("Create Random Number?")
        btn.setStyleSheet("background-color:yellow")
        btn.setFont(QFont("Sanserif", 14))
        btn.clicked.connect(self.rand_generator)
        vbox.addWidget(btn)

        self.setLayout(vbox)

    def rand_generator(self):
        ran = randint(1, 500)
        self.lcd.display(ran)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

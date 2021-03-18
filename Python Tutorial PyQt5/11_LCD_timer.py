import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, \
    QRadioButton, QDialog, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, QTime, QTimer


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        timer = QTimer()
        timer.timeout.connect(self.LCD)

        timer.start(1000)
        # in ms

        self.LCD()

    def LCD(self):
        vbox = QVBoxLayout()

        lcd = QLCDNumber()
        lcd.setStyleSheet("background-color:gray")
        vbox.addWidget(lcd)

        time = QTime.currentTime()
        text = time.toString("hh:mm")
        # convert time to a string

        lcd.display(text)

        self.setLayout(vbox)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

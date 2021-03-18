import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, \
    QRadioButton, QDialog, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

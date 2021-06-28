import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        self.msg_box()

    def msg_box(self):
        hbox = QHBoxLayout()

        btn1 = QPushButton("Warning")
        btn2 = QPushButton("Info")
        btn3 = QPushButton("About")
        btn4 = QPushButton("Yes/No")

        btn1.clicked.connect(self.warning_msg)
        btn2.clicked.connect(self.info_msg)
        btn3.clicked.connect(self.about_msg)
        btn4.clicked.connect(self.yn_msg)

        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        hbox.addWidget(btn4)

        vbox = QVBoxLayout()
        self.label = QLabel("")
        self.label.setFont(QFont("Sanserif", 12))

        vbox.addLayout(hbox)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

    def warning_msg(self):
        QMessageBox.warning(self, "Warning", "You goofed")

    def info_msg(self):
        QMessageBox.information(self, "Info", "Okie")

    def about_msg(self):
        QMessageBox.about(self, "About", "You about to be goofed")

    def yn_msg(self):
        msg = QMessageBox.question(self, "Choice Message", "Do you goof?", QMessageBox.Yes | QMessageBox.No)
            
        if msg == QMessageBox.Yes:
            self.label.setText("I love you!")
        elif msg == QMessageBox.No:
            self.label.setText("Goof off!")
        else:
            self.label.setText("WTF?")



app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

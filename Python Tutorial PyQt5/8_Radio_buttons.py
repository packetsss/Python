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

        self.label = QLabel("")
        self.label.setFont(QFont("Sanserif", 14))

        self.crt_radio_btn()

    def crt_radio_btn(self):
        groupbox = QGroupBox("What's ur sportsmanship??")
        groupbox.setFont(QFont("Sanserif", 15))

        hbox = QHBoxLayout()

        rbtn1 = QRadioButton("Soccer")
        rbtn1.setChecked(True)
        rbtn1.setIcon(QIcon("src\\shoe.png"))
        rbtn1.setIconSize(QSize(40, 40))
        rbtn1.setFont(QFont("Sanserif", 14))
        rbtn1.toggled.connect(self.select)

        rbtn2 = QRadioButton("Baseball")
        rbtn2.setIcon(QIcon("src\\ball.png"))
        rbtn2.setIconSize(QSize(40, 40))
        rbtn2.setFont(QFont("Sanserif", 14))
        rbtn2.toggled.connect(self.select)

        rbtn3 = QRadioButton("Football")
        rbtn3.setIcon(QIcon("src\\landscape.jpg"))
        rbtn3.setIconSize(QSize(40, 40))
        rbtn3.setFont(QFont("Sanserif", 14))
        rbtn3.toggled.connect(self.select)

        rbtn4 = QRadioButton("Basketball")
        rbtn4.setIcon(QIcon("src\\chessboard.png"))
        rbtn4.setIconSize(QSize(40, 40))
        rbtn4.setFont(QFont("Sanserif", 14))
        rbtn4.toggled.connect(self.select)

        hbox.addWidget(rbtn1)
        hbox.addWidget(rbtn2)
        hbox.addWidget(rbtn3)
        hbox.addWidget(rbtn4)
        groupbox.setLayout(hbox)
        # Group everything in the group box

        vbox = QVBoxLayout()
        vbox.addWidget(groupbox)
        vbox.addWidget(self.label)
        # Group the group box in the vbox

        self.setLayout(vbox)
        # display vbox

    def select(self):
        rbtn = self.sender()

        if rbtn.isChecked():
            self.label.setText(f"You have selected: {rbtn.text()}")


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

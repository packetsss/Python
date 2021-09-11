# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, \
    QRadioButton, QDialog, QLabel, QLineEdit, QSpinBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))

        self.spin_box()

    def spin_box(self):
        hbox = QHBoxLayout()
        label = QLabel("Laptop Price: ")

        self.lineEdit = QLineEdit()
        self.spinbox = QSpinBox()
        self.spinbox.valueChanged.connect(self.price)

        self.tot = QLineEdit()

        hbox.addWidget(label)
        hbox.addWidget(self.lineEdit)
        hbox.addWidget(self.spinbox)
        hbox.addWidget(self.tot)

        self.setLayout(hbox)

    def price(self):
        if self.lineEdit.text():
            price = int(self.lineEdit.text())
            # get the input value
            tot = self.spinbox.value() * price
            self.tot.setText(str(tot))
        else:
            print("Wrong Value")


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

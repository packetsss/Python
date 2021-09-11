# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon

class Window(QWidget):
    # inherent from QWidget(base class) || QDialog || QMainWindow

    def __init__(self):
        super().__init__()
        # makes inheritance more manageable

        self.setGeometry(200, 200, 400, 300)
        # window size --> location_x, location_y, width, height

        self.setWindowTitle("I love AJ")
        self.setWindowIcon(QIcon("src\\fruit.ico"))
        # use QIcon inside set

        '''
        self.setFixedWidth(400)
        self.setFixedHeight(200)
        # make it un-resizeable

        self.setWindowOpacity(0.8)
        # change transparency

        self.setStyleSheet("background-color: green
        # change bg color
        '''

        self.create_btn()
        self.show()

    def create_btn(self):
        btn1 = QPushButton("Click me...", self)

        btn1.setGeometry(50, 50, 100, 100)
        btn1.move(100, 100)
        # change size and position
        btn1.setIcon(QIcon("src\\ball.png"))
        btn1.setStyleSheet("background-color:yellow")

        btn1.clicked.connect(self.clicked_btn)
        # assign signals to the button

        btn2 = QPushButton("Click me too...", self)
        btn2.setGeometry(200, 100, 100, 100)
        btn2.setIcon(QIcon("src\\soccer.jpeg"))
        btn2.setStyleSheet("background-color:gray")
        btn2.clicked.connect(self.clicked_btn2)

    def clicked_btn(self):
        print("Button 1 clicked")

    def clicked_btn2(self):
        print("Button 2 clicked")


app = QApplication(sys.argv)
window = Window()
# or window.show()
app.exec_()

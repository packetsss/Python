from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import uic
import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\my_button.ui", self)

        button = self.findChild(QPushButton, "pushButton")
        # find the named button
        button.clicked.connect(self.clicked_btn)

    def clicked_btn(self):
        print("1 clicked!")


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()


# How to convert .ui files to .py

# cd C:\Users\pyjpa\miniconda3\Scripts

# python -m PyQt5.uic.pyuic -x [name].ui -o [name].py


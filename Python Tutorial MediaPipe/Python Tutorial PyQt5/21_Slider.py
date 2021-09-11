# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\Slider.ui", self)

        self.slider = self.findChild(QSlider, "horizontalSlider")
        self.slider.valueChanged.connect(self._slider)
        self.label = self.findChild(QLabel, "label_2")

    def _slider(self):
        value = self.slider.value()
        self.label.setText(f"Value: {value}")


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()

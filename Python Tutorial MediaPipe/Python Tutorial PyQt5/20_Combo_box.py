# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\Combo_box.ui", self)

        self.combo = self.findChild(QComboBox, "comboBox")
        self.label = self.findChild(QLabel, "label")
        item = self.combo.currentText()
        self.label.setText(f"You selected: {item}")

        self.combo.currentTextChanged.connect(self.combo_selected)

    def combo_selected(self):
        item = self.combo.currentText()
        self.label.setText(f"You selected: {item}")


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()

# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint


class Window(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\Calendar.ui", self)

        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.label = self.findChild(QLabel, "label")
        self.label.setText(f"Date is: {str(self.calendar.selectedDate().toPyDate())}")

        self.calendar.selectionChanged.connect(self.date)

    def date(self):
        date_sel = self.calendar.selectedDate()

        string = str(date_sel.toPyDate())
        # convert to string

        self.label.setText(f"Date is: {string}")


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

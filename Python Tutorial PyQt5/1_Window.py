import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)
# initialize app, sys.argv is not required

window = QWidget()
# created window
window.show()
# show window


app.exec_()
# mainloop

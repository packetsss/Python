# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(866, 590)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.print_file)
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.print_preview_dialog)
        self.horizontalLayout.addWidget(self.pushButton_2)
        
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Print File"))
        self.pushButton_2.setText(_translate("Form", "Print Preview"))

    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def print_preview_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        pre = QPrintPreviewDialog(printer, self)
        pre.paintRequested.connect(self.print_preview)
        pre.exec_()

    def print_preview(self, printer):
        self.textEdit.print_(printer)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

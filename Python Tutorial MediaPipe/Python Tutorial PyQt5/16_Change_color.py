# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog, QFontDialog


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(749, 633)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.color = QtWidgets.QPushButton(Form)
        self.color.setObjectName("color")
        self.color.clicked.connect(self.color_dialog)
        self.horizontalLayout_2.addWidget(self.color)

        self.font = QtWidgets.QPushButton(Form)
        self.font.setObjectName("font")
        self.font.clicked.connect(self.font_dialog)
        self.horizontalLayout_2.addWidget(self.font)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "CHANGE"))
        self.color.setText(_translate("Form", "Change Color"))
        self.font.setText(_translate("Form", "Change Font"))

    def color_dialog(self):
        color = QColorDialog.getColor()
        print(color.name())
        self.textEdit.setTextColor(color)

    def font_dialog(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

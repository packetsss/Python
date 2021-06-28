from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self, Form):
        Form.setObjectName("Form")
        Form.resize(970, 659)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dial = QtWidgets.QDial(Form)
        self.dial.setStyleSheet("QDial{\n"
                                "    background-color: rgb(170, 170, 255);\n"
                                "}")
        self.dial.setObjectName("dial")
        self.dial.valueChanged.connect(self.dial_changed)
        self.dial.setMaximum(3600)
        # add some smoothness

        self.verticalLayout.addWidget(self.dial)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{\n"
                                 "    color: red;\n"
                                 "}")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def dial_changed(self):
        value = self.dial.value()
        self.label.setText(f"Dial is changing: {value}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form(Form)
    Form.show()
    sys.exit(app.exec_())

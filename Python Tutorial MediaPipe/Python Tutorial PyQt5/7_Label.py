# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QFont("Sanserif", 15))
        self.label_2.setStyleSheet("color: red")
        # change font, color --> text color, background-color

        self.horizontalLayout_2.addWidget(self.label_2)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clicked)

        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Inputs"))
        self.label.setText(_translate("Form", "Name:"))
        self.label_2.setText(_translate("Form", "labelResult"))
        self.pushButton.setText(_translate("Form", "Click"))

    def clicked(self):
        name = self.lineEdit.text()
        self.label_2.setText(name)
        # assign name to the label


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

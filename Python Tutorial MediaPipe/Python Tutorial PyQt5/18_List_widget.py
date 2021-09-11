# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(938, 593)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListWidget{\n"
                                      "    color: rgb(170, 85, 255);\n"
                                      "    font: 75 16pt \"MS Shell Dlg 2\";\n"
                                      "    background-color: rgb(197, 255, 255);\n"
                                      "}")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.listWidget.clicked.connect(self.item_clicked)
        
        self.verticalLayout.addWidget(self.listWidget)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
                                 "color:rgb(255, 85, 0)\n"
                                 "}")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "List"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Form", "Python"))
        item = self.listWidget.item(1)
        item.setText(_translate("Form", "Java"))
        item = self.listWidget.item(2)
        item.setText(_translate("Form", "C++"))
        item = self.listWidget.item(3)
        item.setText(_translate("Form", "C#"))
        item = self.listWidget.item(4)
        item.setText(_translate("Form", "JavaScript"))
        item = self.listWidget.item(5)
        item.setText(_translate("Form", "Kotlin"))
        self.listWidget.setSortingEnabled(__sortingEnabled)

    def item_clicked(self):
        item = self.listWidget.currentItem()
        self.label.setText(f"You have selected: {item.text()}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

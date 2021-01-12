# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'face_recognition.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QToolTip, QPushButton, QMessageBox)
from PyQt5.QtCore import QCoreApplication, Qt
import os

class Ui_Dialog(object):
    def runcode(self,Dialog):
        self.label_4.setText("Started")
        #Dialog.show()
        os.system("python3.7 facerec.py")
        self.label_4.setText( "Ended")
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        #Dialog.resize(800, 600)
        #Dialog.showMaximized()
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 150, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.runcode)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 10, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(560, 20, 200, 16))
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 650, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(145, 650, 68, 17))
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(1150, 650, 99, 27))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "INITATE "))
        self.label.setText(_translate("Dialog", "FACE RECOGNITION"))
        self.label_2.setText(_translate("Dialog", "Code Status :"))
        self.label_4.setText(_translate("Dialog", "Ready"))
        self.pushButton_2.setText(_translate("Dialog", "Close"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.showMaximized()
    Dialog.show()

    def update_label():
        f1 = open("record/name.txt", "r")
        name = f1.read()
        ui.label_4.setText(name)


    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\usuario\OneDrive\Documentos\semestre 2021-3\ciencias 2.2\Recorrido\ventanaE.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(470, 345)
        self.boton_Agregar = QtWidgets.QPushButton(Dialog)
        self.boton_Agregar.setGeometry(QtCore.QRect(300, 300, 75, 23))
        self.boton_Agregar.setObjectName("boton_Agregar")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(60, 40, 341, 251))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.boton_Agregar.setText(_translate("Dialog", "Agregar"))

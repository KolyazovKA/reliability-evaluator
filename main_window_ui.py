# -*- coding: utf-8 -*-
import sys

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(777, 566)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.open_file = QtWidgets.QPushButton(self.centralwidget)
		self.open_file.setObjectName("open_file")
		self.horizontalLayout.addWidget(self.open_file)
		self.save_in_file = QtWidgets.QPushButton(self.centralwidget)
		self.save_in_file.setObjectName("save_in_file")
		self.horizontalLayout.addWidget(self.save_in_file)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.graph = QtWidgets.QWidget(self.centralwidget)
		self.graph.setMinimumSize(QtCore.QSize(0, 400))
		self.graph.setObjectName("graph")
		self.verticalLayout.addWidget(self.graph)
		self.input_parameters = QtWidgets.QPushButton(self.centralwidget)
		self.input_parameters.setObjectName("input_parameters")
		self.verticalLayout.addWidget(self.input_parameters)
		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.open_file.setText(_translate("MainWindow", "Открыть"))
		self.save_in_file.setText(_translate("MainWindow", "Сохранить"))
		self.input_parameters.setText(_translate("MainWindow", "Ввести параметры"))


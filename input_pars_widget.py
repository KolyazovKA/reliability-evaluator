import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import QtCore
from input_params_ui import Ui_Input_params
class InputParamsWidget(QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Input_params()
		self.ui.setupUi(self)
		self.min_count_of_nodes_values = None
		self.max_count_of_nodes_values = None
		self.parameter_values = None

		self.ui.min_count_of_nodes.activated.connect(self.update_max_nodes)
		self.ui.build_graph.clicked.connect(self.accept)
	def get_values(self):
		return self.min_count_of_nodes_values, self.max_count_of_nodes_values, self.parameter_values
	def update_max_nodes(self):
		self.ui.max_count_of_nodes.clear()
		min_nodes_index = self.ui.min_count_of_nodes.currentIndex()

		for i in range(min_nodes_index + 1, 52):
			self.ui.max_count_of_nodes.addItem("")
		for j in range(min_nodes_index + 1, 52):
			self.ui.max_count_of_nodes.setItemText(j - min_nodes_index - 1,
			                                    QtCore.QCoreApplication.translate("Input_params", str(j + 3)))

	def accept(self):
		if self.ui.parameter.text() == "":
			QMessageBox.warning(self, "Ошибка", "Введите параметр формирования графа")
			return
		try:
			value = float(self.ui.parameter.text())
			if value < 0 or value > 1:
				QMessageBox.warning(self, "Ошибка", "Неправильное значение параметра. \n"
				                                             "Корректное значение лежит в промежутке между 0 и 1")
				return
		except ValueError:
			QMessageBox.warning(self, "Ошибка", "Неправильное значение параметра. \n"
			                                             "Корректное значение лежит в промежутке между 0 и 1")
			return
		# print("Ok")
		self.min_count_of_nodes_values = self.ui.min_count_of_nodes.currentText()
		self.max_count_of_nodes_values = self.ui.max_count_of_nodes.currentText()
		self.parameter_values = self.ui.parameter.text()
		super().accept()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = InputParamsWidget()
	window.exec()

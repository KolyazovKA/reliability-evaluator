import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from input_pars_widget import InputParamsWidget
from main_window_ui import Ui_MainWindow
from reliability_evaluator import ReliabilityEvaluator


class MyApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.min_nodes = None
		self.max_nodes = None
		self.parameter = None

		self.input_parameters.clicked.connect(self.show_input_params)
		# self.save_in_file.clicked.connect(self.save_in_file)
		self.open_file.clicked.connect(self.open_file_dialog)

	def save_in_file(self):
		pass
	def open_file_dialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.ReadOnly

		file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt);;All Files (*)",
		                                           options=options)

		if file_name:
			self.read_file(file_name)

	def read_file(self, file_name):
		try:
			with open(file_name, 'r') as file:
				# Читаем минимальное и максимальное количество узлов
				min_max_nodes_line = file.readline().strip().split()
				min_nodes = int(min_max_nodes_line[0])
				max_nodes = int(min_max_nodes_line[1])

				# Читаем значения оценки надежности
				reliability_values_line = file.readline().strip().split()
				reliability_values = [float(value) for value in reliability_values_line]

				# Теперь у вас есть min_nodes, max_nodes и reliability_value, и вы можете использовать их по своему усмотрению
				self.build_graph_from_file(min_v=min_nodes, max_v=max_nodes, reliablities=reliability_values)

		except Exception as e:
			print("Error reading file:", e)

	def get_values(self, min_v, max_v, p):
		self.min_nodes = min_v
		self.max_nodes = max_v
		self.parameter = p

	def build_graph_from_file(self, min_v=None, max_v=None, reliablities=None):
		# Инициализация объекта Figure и холста для графика
		self.figure, self.ax = self.init_plot()
		self.canvas = FigureCanvas(self.figure)

		self.graph_layout = QVBoxLayout(self.graph)
		self.graph_layout.addWidget(self.canvas)

		self.plot_from_file(min_v, max_v, reliablities)


	def plot_from_file(self, min_value=None, max_value=None, reliabilities=None):
		x, y = [], []
		for i in range(min_value, max_value+1):
			x.append(i)
		for i in reliabilities:
			y.append(i)
		self.ax.plot(x, y)
		self.ax.set_title("График зависимости оценки надежности от числа узлов")
		self.ax.set_xlabel("Число узлов")
		self.ax.set_ylabel("Оценка надежности")
		self.canvas.draw()
	def build_graph_in_main_window(self, min_v=None, max_v=None, p=None):
		# Инициализация объекта Figure и холста для графика
		self.figure, self.ax = self.init_plot()
		self.canvas = FigureCanvas(self.figure)

		self.graph_layout = QVBoxLayout(self.graph)
		self.graph_layout.addWidget(self.canvas)

		self.plot_example(min_v, max_v, p)

	def init_plot(self):
		figure = Figure()
		ax = figure.add_subplot(111)
		return figure, ax

	def plot_example(self, min_value=None, max_value=None, p=None):
		g = ReliabilityEvaluator()
		x, y = g.generate_x_y(min_n=min_value, max_n=max_value, p=p)
		self.ax.plot(x, y)
		self.ax.set_title("График зависимости оценки надежности от числа узлов")
		self.ax.set_xlabel("Число узлов")
		self.ax.set_ylabel("Оценка надежности")
		self.canvas.draw()


	def show_input_params(self):
		input_params_dialog = InputParamsWidget()
		# input_params_ui = InputParamsWidget()
		# input_params_ui.setupUi(input_params_dialog)
		input_params_dialog.exec()


		min_v, max_v, p = input_params_dialog.get_values()
		if min_v is not None and max_v is not None and p is not None:
			print("OK")
			print("Values:", min_v, max_v, p)
			self.get_values(min_v, max_v, p)
			print(self.min_nodes, self.max_nodes, self.parameter)
			self.build_graph_in_main_window(self.min_nodes, self.max_nodes,self.parameter)
			# Закрытие виджета после обработки данных
			# input_params_dialog.close()
		else:
			print("Failed")



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())

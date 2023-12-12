import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, \
	QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from input_pars_widget import InputParamsWidget
from main_window_ui import Ui_MainWindow
from reliability_evaluator import ReliabilityEvaluator


class MyApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# Основные параметры
		self.min_nodes = None # Минимальное количество узлов
		self.max_nodes = None # Максильное количество узлов
		self.parameter = None # Параметр для формирования случайного графа
		self.points = None # Массив со значениями оценок надежности

		# Инициализация графика
		self.figure, self.ax = self.init_plot()
		self.canvas = FigureCanvas(self.figure)
		self.graph_layout = QVBoxLayout(self.graph)
		self.graph_layout.addWidget(self.canvas)

		# Обработка нажатий на кнопки
		self.input_parameters.clicked.connect(self.show_input_params)
		self.open_file.clicked.connect(self.open_file_dialog)
		self.save_in_file.clicked.connect(self.save_info_in_file)

	def save_info_in_file(self):
		"""
		Сохранение значений в файл.

		:return: None
		"""
		if self.min_nodes is None and self.max_nodes is None and self.parameter is None:
			QMessageBox.warning(
				self.parent(),
				"Ошибка сохранения информации в файл",
				"Нечего сохранять. Сначала сгенерируйте граф",
				QMessageBox.Ok
			)
			return

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file_path, _ = QFileDialog.getSaveFileName(
			self.parent(),
			"Сохранить файл",
			"",
			"Text Files (*.txt);;All Files (*)",
			options=options
		)

		# Если пользователь отменил диалог сохранения файла, вернуться
		if not file_path:
			return

		try:
			with open(file_path, 'w') as file:
				# Запись минимального и максимального количества узлов
				file.write(f"{self.min_nodes} {self.max_nodes}\n")

				# Запись значений оценок надежности
				file.write(" ".join(map(str, self.points)))

			QMessageBox.information(
				self.parent(),
				"Информация сохранена",
				"Информация успешно сохранена в файл",
				QMessageBox.Ok
			)

		except Exception as e:
			QMessageBox.warning(
				self.parent(),
				"Ошибка сохранения информации в файл",
				f"Произошла ошибка при сохранении файла: {str(e)}",
				QMessageBox.Ok
			)

	def open_file_dialog(self):
		"""
		Открываем файл и читаем информацию из него.

		:return: None
		"""

		# Открытие проводника
		options = QFileDialog.Options()
		options |= QFileDialog.ReadOnly
		file_name, _ = QFileDialog.getOpenFileName(
			self,
			"Выберите файл",
			"",
			"Text Files (*.txt);;All Files (*)",
			options=options
		)

		# Чтение информации из файла
		if file_name:
			self.read_file(file_name)

	def read_file(self, file_name):
		"""
		Чтение информации из файла.

		:param file_name: Имя файла (str)
		:return: None
		"""
		try:
			with open(file_name, 'r') as file:
				# Читаем минимальное и максимальное количество узлов
				min_max_nodes_line = file.readline().strip().split()
				min_nodes = int(min_max_nodes_line[0])
				max_nodes = int(min_max_nodes_line[1])

				# Читаем значения оценки надежности
				reliability_values_line = file.readline().strip().split()
				reliability_values = [float(value) for value in reliability_values_line]

				# Теперь у вас есть min_nodes, max_nodes и reliability_value,
				# и вы можете использовать их по своему усмотрению
				self.plot_from_file(min_nodes, max_nodes, reliability_values)

		except Exception as e:
			print("Error reading file:", e)
			QMessageBox.warning(
				self.parent(),
				"Ошибка чтения файла",
				f"Произошла ошибка при чтении файла: {str(e)}",
				QMessageBox.Ok
			)

	def get_values(self, min_v, max_v, p):
		"""
		Запись в параметры значений минимального, максимального числа узлов и параметра
		для формирования случайного графа.

		:param min_value: Минимальное количество узлов (int)
		:param max_value: Максимальное количество узлов (int)
		:param reliabilities: Список значений надежности (float)
		:return: None
		"""
		self.min_nodes = int(min_v)
		self.max_nodes = int(max_v)
		self.parameter = float(p)

	def plot_from_file(self, min_value=None, max_value=None, reliabilities=None):
		"""
		Построение графика с использованием информации из файла.

		:param min_value: Минимальное количество узлов (int)
		:param max_value: Максимальное количество узлов (int)
		:param reliabilities: Список значений надежности (float)
		:return: None
		"""
		self.ax.clear()  # Очистка существующего графика
		x, y = [], []
		for i in range(min_value, max_value + 1):
			x.append(i)
		for i in reliabilities:
			y.append(i)
		self.ax.plot(x, y)
		self.ax.set_title("График зависимости оценки надежности от числа узлов")
		self.ax.set_xlabel("Число узлов")
		self.ax.set_ylabel("Оценка надежности")
		self.canvas.draw()

	def init_plot(self):
		"""
		Инициализация нового графика.

		:return: Кортеж, содержащий объекты Figure и Axes
		"""
		figure = Figure()
		ax = figure.add_subplot(111)
		return figure, ax

	def plot(self, min_value=None, max_value=None, p=None):
		"""
		Построение графика с использованием информации о надежности, сгенерированной ReliabilityEvaluator.

		:param min_value: Минимальное количество узлов (int)
		:param max_value: Максимальное количество узлов (int)
		:param p: Параметр для расчета надежности (float)
		:return: None
		"""
		self.ax.clear()  # Очистка существующего графика
		g = ReliabilityEvaluator()
		x, y = g.generate_x_y(min_n=min_value, max_n=max_value, p=p)
		self.points = y
		self.ax.plot(x, y)
		self.ax.set_title("График зависимости оценки надежности от числа узлов")
		self.ax.set_xlabel("Число узлов")
		self.ax.set_ylabel("Оценка надежности")
		self.canvas.draw()

	def show_input_params(self):
		"""
		Отображение диалогового окна для ввода параметров и построение графика.

		:return: None
		"""
		input_params_dialog = InputParamsWidget()
		input_params_dialog.exec()

		min_v, max_v, p = input_params_dialog.get_values()
		if min_v is not None and max_v is not None and p is not None:
			self.get_values(min_v, max_v, p)
			self.plot(self.min_nodes, self.max_nodes, self.parameter)
		else:
			print("Не удалось выполнить")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())

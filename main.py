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
		self.min_nodes = None
		self.max_nodes = None
		self.parameter = None
		self.points = None

		# Initialize canvas and layout
		self.figure, self.ax = self.init_plot()
		self.canvas = FigureCanvas(self.figure)
		self.graph_layout = QVBoxLayout(self.graph)
		self.graph_layout.addWidget(self.canvas)

		self.input_parameters.clicked.connect(self.show_input_params)
		self.open_file.clicked.connect(self.open_file_dialog)
		self.save_in_file.clicked.connect(self.save_info_in_file)

	def save_info_in_file(self):
		if self.min_nodes is None and self.max_nodes is None and self.parameter is None:
			QMessageBox.warning(self.parent(), "Ошибка сохранения информации в файл", "Нечего сохранять. Сначала сгенерируйте граф", QMessageBox.Ok)
			return

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file_path, _ = QFileDialog.getSaveFileName(self.parent(), "Сохранить файл", "", "Text Files (*.txt);;All Files (*)",
		                                           options=options)

		# If the user canceled the file dialog, return
		if not file_path:
			return

		try:
			# Open the selected file for writing
			with open(file_path, 'w') as file:
				# Write parameters on the first line
				file.write(f"{self.min_nodes} {self.max_nodes}\n")

				# Write points on the next line
				file.write(" ".join(map(str, self.points)))

			QMessageBox.information(self.parent(), "Информация сохранена", "Информация успешно сохранена в файл",
			                        QMessageBox.Ok)

		except Exception as e:
			QMessageBox.warning(self.parent(), "Ошибка сохранения информации в файл",
			                    f"Произошла ошибка при сохранении файла: {str(e)}", QMessageBox.Ok)


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
			QMessageBox.warning(self.parent(), "Ошибка чтения файла", f"Произошла ошибка при чтении файла: {str(e)}",
			                    QMessageBox.Ok)

	def get_values(self, min_v, max_v, p):
		self.min_nodes = int(min_v)
		self.max_nodes = int(max_v)
		self.parameter = float(p)

	def build_graph_from_file(self, min_v=None, max_v=None, reliablities=None):
		# Инициализация объекта Figure и холста для графика
		# self.figure, self.ax = self.init_plot()
		# self.canvas = FigureCanvas(self.figure)
		#
		# self.graph_layout = QVBoxLayout(self.graph)
		# self.graph_layout.addWidget(self.canvas)

		self.plot_from_file(min_v, max_v, reliablities)


	def plot_from_file(self, min_value=None, max_value=None, reliabilities=None):
		self.ax.clear()  # Clear existing plot
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

	def build_graph_in_main_window(self, min_v=None, max_v=None, p=None):
		# Инициализация объекта Figure и холста для графика
		# self.figure, self.ax = self.init_plot()
		# self.canvas = FigureCanvas(self.figure)
		#
		# self.graph_layout = QVBoxLayout(self.graph)
		# self.graph_layout.addWidget(self.canvas)

		self.plot(min_v, max_v, p)

	def init_plot(self):
		figure = Figure()
		ax = figure.add_subplot(111)
		return figure, ax

	def plot(self, min_value=None, max_value=None, p=None):
		self.ax.clear()  # Clear existing plot
		g = ReliabilityEvaluator()
		x, y = g.generate_x_y(min_n=min_value, max_n=max_value, p=p)
		self.points = y
		self.ax.plot(x, y)
		self.ax.set_title("График зависимости оценки надежности от числа узлов")
		self.ax.set_xlabel("Число узлов")
		self.ax.set_ylabel("Оценка надежности")
		self.canvas.draw()


	def show_input_params(self):
		input_params_dialog = InputParamsWidget()
		input_params_dialog.exec()

		min_v, max_v, p = input_params_dialog.get_values()
		if min_v is not None and max_v is not None and p is not None:
			self.get_values(min_v, max_v, p)
			self.build_graph_in_main_window(self.min_nodes, self.max_nodes,self.parameter)
		else:
			print("Failed")



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())

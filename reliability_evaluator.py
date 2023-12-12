import numpy as np
from graph import Graph


class ReliabilityEvaluator(Graph):

	def generate_x_y(self, min_n, max_n, p):
		"""
		Генерация точек для построения графа.

		:param min_n: Минимальное количество узлов (int)
		:param max_n: Максимальное количество узлов (int)
		:param p: Параметр для расчета надежности (float)
		:return: Кортеж из массивов x и y для построения графика
		"""
		x = np.arange(min_n, max_n + 1)
		y = np.empty_like(x, dtype=float)
		for i in range(min_n, max_n + 1):
			reliable = 0
			self._inputs(i, p)
			for j in range(10):
				self._generate_graph()
				reliable += self._reliability_calculation()
			result = reliable / 10
			y[i - min_n] = result
		return x, y

	def find_node_with_most_connections(self):
		"""
		Поиск точки сочленения.

		:return: Номер узла с наибольшим количеством связей
		"""
		max_connections = 0
		node_with_most_connections = None

		for i, row in enumerate(self.graph):
			connections = sum(row)
			if connections > max_connections:
				max_connections = connections
				node_with_most_connections = i

		return node_with_most_connections

	def _reliability_calculation(self):
		"""
		Расчет оценки надежности.

		:return: Значение оценки надежности
		"""
		connections = 0

		for i, row in enumerate(self.graph):
			if i != self.find_node_with_most_connections():
				connections += sum(row)

		return connections / (self.nodes * (self.nodes - 1))


def main():
	g = ReliabilityEvaluator()
	g._inputs(10, 0.75)
	g._generate_graph()
	g._print_graph()

	print(g.find_node_with_most_connections())
	print(g._reliability_calculation())
	print(g.generate_x_y(3, 10, 0.75))


if __name__ == '__main__':
	main()

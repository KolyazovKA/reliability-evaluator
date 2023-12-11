from random import randint

import numpy as np

from graph import Graph


class ReliabilityEvaluator(Graph):

	def generate_x_y(self, min_n, max_n, p):
		x = np.arange(min_n, max_n)
		y = np.empty_like(x, dtype=float)
		for i in range(min_n, max_n):
			self._inputs(i, p)
			self._generate_graph()
			y[i - min_n] = self._reliability_calculation()
		return x, y


	def find_node_with_most_connections(self):
		max_connections = 0
		node_with_most_connections = None

		for i, row in enumerate(self.graph):
			connections = sum(row)
			if connections > max_connections:
				max_connections = connections
				node_with_most_connections = i

		return node_with_most_connections

	def _reliability_calculation(self):
		connections = 0

		for i, row in enumerate(self.graph):
			if i != self.find_node_with_most_connections():
				connections += sum(row)

		return (connections / (self.nodes * (self.nodes - 1)))


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

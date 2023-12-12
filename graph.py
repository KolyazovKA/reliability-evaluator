import random
class Graph:
    def __init__(self):
        self.graph = None
        self.nodes = None
        self.p = None

        self.current_seed = 0

    def _inputs(self, nodes, p):
        """
        Установка значений числа узлов и параметра для расчета надежности.

        :param nodes: Количество узлов (int)
        :param p: Параметр для расчета надежности (float)
        :return: None
        """
        self.nodes = nodes
        self.p = p

    def get_graph(self):
        """
        Получение текущего графа.

        :return: Матрица смежности текущего графа
        """
        return self.graph

    def _generate_graph(self):
        """
        Генерация случайного графа.

        :return: None
        """
        self.current_seed += 1
        random.seed(self.current_seed)
        self.graph = [[0 for j in range(self.nodes)] for i in range(self.nodes)]
        for i in range(self.nodes):
            for j in range(self.nodes):
                n = random.randint(0, 100)
                if n <= int(self.p * 100) and i != j:
                    self.graph[i][j] = 1
                else:
                    self.graph[i][j] = 0

    def _print_graph(self):
        """
        Вывод графа в консоль.

        :return: None
        """
        for row in self.graph:
            print(row)


def main():
    g = Graph()
    g._inputs(10, 0.5)
    g._generate_graph()
    g._print_graph()


if __name__ == "__main__":
    main()

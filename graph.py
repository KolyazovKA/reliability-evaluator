import random
class Graph:
    def __init__(self):
        self.graph = None
        self.nodes = None
        self.p = None

    def _inputs(self, nodes, p):
        self.nodes = nodes
        self.p = p

    def get_graph(self):
        return self.graph
    def _generate_graph(self):
        self.graph = [[0 for j in range(self.nodes)] for i in range(self.nodes)]
        for i in range(self.nodes):
            for j in range(self.nodes):
                n = random.randint(0, 100)
                if n <= self.p * 100 and i != j:
                    self.graph[i][j] = 1
                else: self.graph[i][j] = 0

    def _print_graph(self):
        for row in self.graph:
            print(row)


def main():
    g = Graph()
    g._inputs(10, 0.5)
    g._generate_graph()
    g._print_graph()


if __name__ == "__main__":
    main()

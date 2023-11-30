from random import randint
from graph import Graph

class ReliabilityEvaluator(Graph):
    def __find_node_with_most_connections(self):
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
            if i != self.__find_node_with_most_connections():
                connections += sum(row)

        return(connections/(self.nodes * (self.nodes - 1)))

def main():
    g = ReliabilityEvaluator()
    g._inputs(10, 0.9)
    g._generate_graph()
    g._print_graph()

    print(g.__find_node_with_most_connections())
    print(g._reliability_calculation())

if __name__ == '__main__':
    main()
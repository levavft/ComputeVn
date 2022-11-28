from abeliangroup import AbelianGroup, AbelianGroupElement
from random import getrandbits
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, value: AbelianGroupElement, m: int):
        """
        :param value:
        :param m: the layer of the node
        """
        self.value = value
        self.m = m
        self.prehash = getrandbits(128)

    def __eq__(self, other):
        assert isinstance(other, Node)
        return self.value == other.value and self.m == other.m

    def __str__(self):
        # return f"Node<{self.value}, {self.m}>"
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.prehash)


class SumDiGraph:
    def __init__(self, g: AbelianGroup):
        self.g = g
        self.Graph = nx.DiGraph()

    def generate_digraph(self, m: int):
        current_layer_nodes = {Node(self.g.zero, 0)}
        self.Graph.add_nodes_from(current_layer_nodes, m=0)
        next_layer_edges = list()

        for i in range(m + 1):
            for parent in current_layer_nodes:
                for element in self.g.non_zero_elements:
                    new_node = Node(parent.value + element, i + 1)
                    next_layer_edges.append([parent, new_node])

            # merge nodes with the same value
            next_layer_edges.sort(key=lambda x: self.g.order_map[x[1].value])
            for j in range(len(next_layer_edges) - 1):
                if next_layer_edges[j][1] == next_layer_edges[j + 1][1]:
                    next_layer_edges[j+1][1] = next_layer_edges[j][1]

            next_layer_nodes = set(pair[1] for pair in next_layer_edges)
            self.Graph.add_nodes_from(next_layer_nodes, m=-i - 1)
            self.Graph.add_edges_from(next_layer_edges)

            current_layer_nodes = next_layer_nodes
            next_layer_edges = list()

    def _generate_labels(self):
        return {node: str(node) for node in self.Graph}

    def draw(self):
        pos = nx.multipartite_layout(self.Graph, subset_key='m', align='horizontal')
        nx.draw_networkx(self.Graph, pos=pos, node_shape="s", node_color="white", node_size=2000, edge_color="black",
                         arrows=True,
                         with_labels=self._generate_labels())
        plt.show()


def main():
    g = AbelianGroup((2, 2))
    s = SumDiGraph(g)
    s.generate_digraph(4)
    s.draw()


main()




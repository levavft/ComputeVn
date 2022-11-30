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
        self.graph = nx.DiGraph()
        self.m = 0
        self.leafs = {Node(self.g.zero, 0)}

        self.graph.add_nodes_from(self.leafs, m=self.m)

    def _add_digraph_layer(self):
        next_layer_edges = list()
        self.m += 1

        for parent in self.leafs:
            for element in self.g.non_zero_elements:
                new_node = Node(parent.value + element, self.m)
                next_layer_edges.append([parent, new_node])

        # merge nodes with the same value
        next_layer_edges.sort(key=lambda x: self.g.order_map[x[1].value])
        for j in range(len(next_layer_edges) - 1):
            if next_layer_edges[j][1] == next_layer_edges[j + 1][1]:
                next_layer_edges[j + 1][1] = next_layer_edges[j][1]

        next_layer_nodes = set(pair[1] for pair in next_layer_edges)
        self.graph.add_nodes_from(next_layer_nodes, m=-self.m)
        self.graph.add_edges_from(next_layer_edges)

        self.leafs = next_layer_nodes

    def _get_zero_leaf(self):
        for leaf in self.leafs:
            if leaf.value == self.g.zero:
                return leaf

    def _always_has_zero_subsum(self):
        def has_zero_on_all_subpaths(node):
            if nx.get_node_attributes(self.graph, 'm')[node] == 0:
                return False
            if node.value == self.g.zero:
                return True
            for _parent in self.graph.predecessors(node):
                if not has_zero_on_all_subpaths(_parent):
                    return False
            return True

        outer_zero = self._get_zero_leaf()
        if outer_zero is None:
            return True
        for parent in self.graph.predecessors(outer_zero):
            if not has_zero_on_all_subpaths(parent):
                return False
        return True

    def calculate_v(self, max_tries=10):
        lower_bound = self.g.maximal_element_order() + 1
        for _ in range(lower_bound):
            self._add_digraph_layer()  # first layer is always completely non-zero, single value sums...
        for m in range(lower_bound, lower_bound + max_tries):
            # if self.g.limit == (2, 2, 2):
                # self.draw()
            if self._always_has_zero_subsum():
                return m - 1
            self._add_digraph_layer()
            # self.draw()
        return None

    def _generate_labels(self):
        return {node: str(node) for node in self.graph}

    def draw(self):
        pos = nx.multipartite_layout(self.graph, subset_key='m', align='horizontal')
        nx.draw_networkx(self.graph, pos=pos, node_shape="s", node_color="white", node_size=2000, edge_color="black",
                         arrows=True,
                         with_labels=self._generate_labels())
        plt.show()


def main():
    g = AbelianGroup((2, 2))
    s = SumDiGraph(g)
    print(s.calculate_v())


main()




import networkx as nx
from MultinetPy import multinetpy as mp


class Import_Graph:
    def __init__(self):
        pass

    @staticmethod
    def make_graph(node_file, edges_file, layers_file=None):
        nodes = []
        pos = {}
        file = open(node_file)
        for line in file:
            node = line.split(" ")
            nodes.append((node[0], {"name": node[1]}))
        file.close()

        layers = []
        if layers_file:
            file = open(layers_file)
            for line in file:
                layer = line.split(" ")
                layers.append((layer[0], layer[1]))

        edges = []
        file = open(edges_file)
        for line in file:
            edge = line.split(" ")
            edges.append((edge[0], (edge[1], edge[2], {"weight": int(edge[3][:-1])})))# after removing any trailing characters from the original string.
# If layers is not provided (though the condition len(layers) < 0 will always be false), creates a unique set of layer IDs from the edges and converts it to a list

        if len(layers) < 0:
            layers = set((layer[0], "") for layer in edges)
            layers = list(layers)

        graphs = []
        for layer in layers:
            temp_graph = nx.Graph()
            temp_graph.add_nodes_from(nodes)
            temp_graph.add_edges_from(edge[1] for edge in edges if edge[0] == layer[0])
            graphs.append(temp_graph)

        mg = mp.MultiNetPy(list_of_layers=graphs)
        return mg




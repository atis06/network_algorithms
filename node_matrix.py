import numpy as np
from node_model import NodeModel

class NodeMatrix(object):

    def __init__(self, network_size):
        self.__network_size = network_size
        self.__matrix = np.zeros((network_size, network_size))

    def make_edge(self, node1, node2):
        self.__mod_edge(node1, node2, 1)

    def del_edge(self, node1, node2):
        self.__mod_edge(node1, node2, 0)

    def __mod_edge(self, node1, node2, op):
        if type(node1) is NodeModel and type(node2) is NodeModel:
            self.__matrix[node1.id][node2.id] = op
            #self.__matrix[node2.id][node1.id] = op
        if type(node1) is int and type(node2) is int:
            self.__matrix[node1][node2] = op
            #self.__matrix[node2][node1] = op

    def get_node_to_neighbor_ids(self, node):
        neighbors = []
        n_id = node.id if type(node) == NodeModel else node
        for i in range(self.__network_size):
            if self.__matrix[n_id][i]:
                neighbors.append(i)
        return neighbors

    def get_node_from_neighbor_ids(self, node):
        neighbors = []
        n_id = node.id if type(node) == NodeModel else node
        for i in range(self.__network_size):
            if self.__matrix[i][n_id]:
                neighbors.append(i)
        return neighbors

    @property
    def matrix(self):
        return self.__matrix

    @property
    def size(self):
        return self.__network_size
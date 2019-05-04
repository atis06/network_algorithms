import numpy as np

from node_model import NodeModel
from node_matrix import NodeMatrix
from network_model import NetworkModel
import constants

class NetworkBuilder(object):

    def __init__(self):
        self.__nodes = list()
        self.__virtual_nodes = list()
        self.__network_size = None
        self.__node_matrix = None
        pass

    @property
    def nodes(self):
        return self.__nodes

    @property
    def virtual_nodes(self):
        return self.__virtual_nodes

    def read_files(self):
        # open network.txt
        with open("network.txt") as f:
            network_lines = f.readlines()
        network_lines = np.array([x.strip().split() for x in network_lines]).astype(int)
        self.__network_size = len(network_lines[0])
        self.__node_matrix = NodeMatrix(self.__network_size)
        self.__virtual_node_matrix = NodeMatrix(self.__network_size*(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1))

        # open network_functions.txt
        with open("network_functions.txt") as f:
            network_function_lines = f.readlines()
        network_function_lines = [x.strip().split(",") for x in network_function_lines]

        return network_lines, network_function_lines


    @property
    def build_network(self):
        network_lines, network_function_lines = self.read_files()
        for i in range(self.__network_size):
            self.__nodes.append(self.__gen_node_model(i, network_function_lines[i]))
            for j in range(self.__network_size):
                if(network_lines[i][j] == 1):
                    self.__node_matrix.make_edge(i, j)
                    #self.__node_matrix.make_edge(j, i)

        #Initial construction of G'(phase 1)
        for i in range(self.__network_size*(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1)):
            self.__virtual_nodes.append(self.__gen_node_model(i, self.nodes[int(i/(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1))].network_functions, True))

        return NetworkModel(self.__nodes, self.__virtual_nodes, self.__node_matrix, self.__virtual_node_matrix)

    def __gen_node_model(self, id, network_functions, is_virtual=False):
        return NodeModel(id, network_functions, is_virtual)
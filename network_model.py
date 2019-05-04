from node_model import NodeModel
import constants

class NetworkModel(object):
    """
    Network Model which contains the Nodes and the edges in between

    """

    def __init__(self, nodes, virtual_nodes, node_matrix, virtual_node_matrix):
        self.__nodes = nodes
        self.__virtual_nodes = virtual_nodes
        self.__node_matrix = node_matrix
        self.__virtual_node_matrix = virtual_node_matrix

    @property
    def size(self):
        return len(self.__nodes)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def virtual_nodes(self):
        return self.__virtual_nodes

    @property
    def node_matrix(self):
        return self.__node_matrix

    @property
    def virtual_node_matrix(self):
        return self.__virtual_node_matrix



    def get_virtual_nodes_of_node_id(self, node_id):
        r = len(constants.REQUIRED_SERVICE_FUNCTIONS)
        return self.__virtual_nodes[node_id*(r+1):node_id*(r+1)+r+1]
        pass

    def get_nodes_neighbors(self, node: NodeModel):
        ids = self.get_node_ids_neighbors(node.id)
        return [self.__nodes[n_id] for n_id in ids]

    def get_node_ids_neighbors(self, n_id):
        return self.__node_matrix.get_node_neighbor_ids(self.__nodes[n_id])

    pass

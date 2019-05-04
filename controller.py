from network_builder import NetworkBuilder
from view import View
import numpy as np
import networkx as nx
import constants

class Controller(object):

    def __init__(self, start_node: int, end_node: int, render: bool):
        self.__network = NetworkBuilder().build_network
        print("Graph representation build done...\n")
        print("Original node matrix: ")
        print(self.__network.node_matrix.matrix)
        print("######################################################")
        print("Virtual nodes: ")
        print([str(node.parent_id)+"_"+str(node.id%(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1)) for node in self.__network.virtual_nodes])
        print("######################################################")
        pass

        self.__start_node = start_node
        self.__end_node = end_node
        self.view = View(self.__network, render)
        self.view.render(True)

    @property
    def net(self):
        return self.__network

    def run(self):
        self.init_phase_2()
        self.view.render()
        self.pruning()
        self.view.render()
        self.dijkstra()

    def init_phase_2(self):
        rows, cols = np.where(self.__network.node_matrix.matrix != 0)
        edges = zip(rows.tolist(), cols.tolist())

        print("Adding edges to virtual nodes: ")

        for edge in edges:
            v_l = self.__network.nodes[edge[0]]
            v_k = self.__network.nodes[edge[1]]
            v_l_virtual_nodes = self.__network.get_virtual_nodes_of_node_id(v_l.id)
            v_k_virtual_nodes = self.__network.get_virtual_nodes_of_node_id(v_k.id)

            for i, v_l_virtual_node in enumerate(v_l_virtual_nodes):
                j_star = i
                for j, v_k_virtual_node in enumerate(v_k_virtual_nodes):
                    if j>=i:
                        subset = set(constants.REQUIRED_SERVICE_FUNCTIONS[i:j])
                        network_functions_v_k = set(v_k_virtual_node.network_functions)
                        #print("i: ", i, "j: ", j, "sfcs: ", subset, "nf: ", network_functions_v_k)
                        if subset.issubset(network_functions_v_k):
                            j_star = j
                print(v_l_virtual_nodes[i].parent_id,"_",i,"---->",v_k_virtual_nodes[j_star].parent_id,"_",j_star)
                self.__network.virtual_node_matrix.make_edge(v_l_virtual_nodes[i], v_k_virtual_nodes[j_star])
                self.view.render()
        print("######################################################")
        pass

    def pruning(self):
        print("Removing unneccessary nodes:")
        found = False
        while not found:
            found = False
            for node in self.__network.virtual_nodes:
                if node.parent_id != self.__start_node and node.parent_id != self.__end_node and not node.is_removed:
                    to_ids_length = len(self.__network.virtual_node_matrix.get_node_to_neighbor_ids(node))
                    from_ids_length = len(self.__network.virtual_node_matrix.get_node_from_neighbor_ids(node))
                    if to_ids_length == 0 or from_ids_length == 0:
                        for i in range(self.__network.virtual_node_matrix.size):
                            self.__network.virtual_node_matrix.del_edge(i, node.id)
                            self.__network.virtual_node_matrix.del_edge(node.id, i)
                        self.__network.virtual_nodes[node.id].set_is_removed = True
                        self.view.render()
                        print("Removed: ", str(node.parent_id)+"_"+str(node.id%(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1)))
                        found = True

        #remove unneccessary starting and ending nodes
        print("Removing unneccessary starting nodes:")
        found = False
        for id in range(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1):
            if not self.__network.virtual_nodes[id].is_removed:
                if not found:
                    found = True
                else:
                    for i in range(self.__network.virtual_node_matrix.size):
                        self.__network.virtual_node_matrix.del_edge(i, id)
                        self.__network.virtual_node_matrix.del_edge(id, i)
                    self.__network.virtual_nodes[id].set_is_removed = True
                    self.view.render()
                    print("Removed: ", str(self.__network.virtual_nodes[id].parent_id)+"_"+str(id%(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1)))

        print("Removing unneccessary destination nodes:")
        found = False
        for id in range(len(self.__network.virtual_nodes)-1, len(self.__network.virtual_nodes)-1-len(constants.REQUIRED_SERVICE_FUNCTIONS)-1, -1):
            if not self.__network.virtual_nodes[id].is_removed:
                if not found:
                    found = True
                else:
                    for i in range(self.__network.virtual_node_matrix.size):
                        self.__network.virtual_node_matrix.del_edge(i, id)
                        self.__network.virtual_node_matrix.del_edge(id, i)
                    self.__network.virtual_nodes[id].set_is_removed = True
                    self.view.render()
                    print("Removed: ", str(self.__network.virtual_nodes[id].parent_id) + "_" + str(
                        id % (len(constants.REQUIRED_SERVICE_FUNCTIONS) + 1)))
        print("######################################################")
        pass

    def dijkstra(self):
        graph = nx.MultiDiGraph()
        node_matrix = self.__network.virtual_node_matrix.matrix

        rows, cols = np.where(node_matrix != 0)
        edges = zip(rows.tolist(), cols.tolist())
        graph.add_edges_from(edges)
        print("After pruning: ")
        print(node_matrix)
        print("######################################################")
        all_active_node = set(rows).union(cols)


        print("Shortest path with service fuction chaining:")
        for node in nx.dijkstra_path(graph, min(all_active_node), max(all_active_node)):
            print(self.__network.virtual_nodes[node].parent_id)

    pass

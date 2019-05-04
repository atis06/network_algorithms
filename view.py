from network_model import NetworkModel
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import shutil
import constants
from networkx.drawing.nx_pydot import write_dot

class View(object):

    def __init__(self, model: NetworkModel, render: bool):
        if os.path.exists("./graphs"):
            shutil.rmtree('./graphs')
        os.mkdir("./graphs")
        self.c = 0
        self.model = model
        self.graph = nx.MultiDiGraph()
        self.pos = None
        self.make_graph(model)
        self._render = render
        pass

    def render(self, original = False):
        if self._render:
            if original:
                self.make_graph(self.model, True)
                self.show_graph(True)
            else:
                self.make_graph(self.model)
                self.show_graph(False)
        pass

    def make_graph(self, model: NetworkModel, original=False):
        self.graph = nx.MultiDiGraph()
        node_matrix = model.virtual_node_matrix.matrix
        if original:
            node_matrix = model.node_matrix.matrix
        rows, cols = np.where(node_matrix != 0)

        edges = zip(rows.tolist(), cols.tolist())

        self.graph.add_edges_from(edges)
        self.pos = nx.spring_layout(self.graph)

    def show_graph(self, original):
        color_map = []
        for node in self.graph:
                color_map.append('#F4D5BB')
        plt.figure(1, figsize=(16, 11))
        nx.draw_networkx(self.graph, self.pos, node_color=color_map, node_size=500, scale=200, dim=3)
        #plt.savefig("./graphs/"+ str(self.c) + ".png", format="PNG")
        plt.cla()
        plt.clf()
        self.draw_pygraphviz(original)
        self.c = self.c+1
        # plt.show()
        pass

    def draw_pygraphviz(self, original = False):
        a = nx.nx_agraph.to_agraph(self.graph)
        a.node_attr['style'] = 'filled'

        if not original:
            virtual_nodes = self.model.virtual_nodes
            for node in virtual_nodes:
                try:
                    n = a.get_node(node.id)
                    n.attr['fillcolor'] = "#CCCCFF"
                    n.attr['label']=str(node.parent_id)+"_"+str(node.id%(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1))+" "+str(node.network_functions)
                except:
                    pass
        else:
            nodes = self.model.nodes
            for node in nodes:
                try:
                    n = a.get_node(node.id)
                    n.attr['label']=str(node.id)+" "+str(node.network_functions)
                except:
                    pass
        a.layout(prog='dot')  # use dot
        a.draw("./bgraphs/"+str(self.c) + ".png")
        pass
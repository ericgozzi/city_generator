from networkx.algorithms.link_prediction import within_inter_cluster
from pixels import get_blank_picture
from pixels import Picture
from pixels import Color

from .rule import Rule

import networkx as nx

import math


class Graph:

    def __init__(self):
       self.graph = nx.DiGraph()
       self.attributes = {}



    @property
    def edges(self):
        return self.graph.edges()
    
    @property
    def nodes(self):
        return self.graph.nodes()
    

    @property
    def eigenvector_centrality(self) -> dict:
        return nx.eigenvector_centrality(self.graph)
    
    def add_node_attribute(self, node, key, value):
        self.graph.nodes[node][key] = value

    def get_node_attribute(self, node, key):
        return self.graph.nodes[node][key]
    

    def add_edge_attribute(self, node1, node2, key, value):
        self.graph[node1][node2][key] = value

    def get_edge_attribute(self, node1, node2, key):
        return self.graph[node1][node2][key]


    def draw(self, **kwargs) -> Picture:

        graph_type: str = kwargs.get('graph_type', 'KAMADA-KAWAI')
        graph_dimension: int = kwargs.get('graph_dimension', 2)

        spectral_weight: float = kwargs.get('spectral_weight', None)

        show_node: bool = kwargs.get('show_nodes', True)
        node_radius: int = kwargs.get('node_radius', 30)
        node_color: Color = kwargs.get('node_color', Color.WHITE)

        show_label: bool = kwargs.get('show_label', True)
        label_size: bool = kwargs.get('label_size', 20)
        label_color: Color = kwargs.get('label_color', Color.BLACK)

        edge_direction: bool = kwargs.get('edge_direction', True)
        edge_width: int = kwargs.get('edge_width', 2)
        arrowhead_length: int = kwargs.get('arrowhead_length', 20)
        edge_color: Color = kwargs.get('edge_color', Color.WHITE)

        pic_size: int = kwargs.get('pic_size', 2000)
        background_color: Color = kwargs.get('background_color', Color.BLACK)
        invert_colors: bool = kwargs.get('invert_colors', False)

        show_eigenvector: bool = kwargs.get('show_eigenvector', False)

        show_cartouche: bool = kwargs.get('show_cartouche', False)
        cartouche: str = kwargs.get('cartouche', 'Provide cartouche *kwarg')



        scale_factor = pic_size/2-pic_size/20
        pic = get_blank_picture(pic_size, pic_size, background_color)
        pos = self.get_nodes_coordinate(graph_type, dimension=graph_dimension, spectral_weight=spectral_weight)
        edges = self.edges
        for edge in edges:
            p1x = (pos[edge[0]][0]) * scale_factor + pic_size/2
            p1y = (pos[edge[0]][1]) * scale_factor + pic_size/2
            p2x = (pos[edge[1]][0]) * scale_factor + pic_size/2
            p2y = (pos[edge[1]][1]) * scale_factor + pic_size/2

             # Direction vector
            dx = p2x - p1x
            dy = p2y - p1y
            angle = math.atan(dy/dx)

            if dx < 0:
                xds = -1
                xde = 1
            else:
                xds = 1
                xde = -1

            if dy < 0:
                yds = -1
                yde = 1
            else:
                yds = 1
                yde = -1


            # Move start and end points to the edge of the circles
            start = (p1x + abs(math.cos(angle)) * node_radius * xds,
                     p1y + abs(math.sin(angle)) * node_radius * yds)
            end = (p2x + abs(math.cos(angle)) * node_radius * xde,
                   p2y + abs(math.sin(angle)) * node_radius * yde)

            if edge_direction:
                pic.draw_arrow(start, end, width=edge_width, arrowhead_length=arrowhead_length, color = edge_color)
            else:
                pic.draw_line(start, end, width=edge_width, color=edge_color)

        for key in pos.keys():
            center_x: int = pos[key][0] * scale_factor + pic_size/2
            center_y: int = pos[key][1] * scale_factor + pic_size/2
            if show_node:
                pic.draw_circle((center_x, center_y), node_radius, color=node_color)
            if show_label and not show_eigenvector:
                pic.draw_text(key, (center_x, center_y), label_size, color=label_color)
            elif show_label and show_eigenvector:
                eigenvector = self.get_eigenvector_of(key)
                pic.draw_text(f'{key}\n{eigenvector}', (center_x, center_y), label_size, color=label_color)
            elif not show_label and show_eigenvector:
                eigenvector = self.get_eigenvector_of(key)
                pic.draw_text(str(eigenvector), (center_x, center_y), label_size, color=label_color)
                
        if show_cartouche:
            pic.draw_text(cartouche, (20, pic.height-label_size - 20), label_size, color=label_color, align = 'left')

        if invert_colors:
            pic.invert_colors()

        return pic



    def add_node(self, node: str):
        """Add a node to the graph."""
        self.graph.add_node(node)


    def add_edge(self, node1: str, node2: str):
        """Add an edge between two nodes."""
        self.graph.add_edge(node1, node2)


    def build_graph_from_rules(self, rules: Rule) -> None:
        for item1, item2 in rules.rules:
            self.graph.add_edge(item1, item2)


    def get_eigenvector_of(self, item) -> float:
        eigenvector_centrality_dictionary = self.eigenvector_centrality
        item_centrality = eigenvector_centrality_dictionary[item]
        return item_centrality



    def get_nodes_coordinate(self, method, dimension=2, spectral_weight=None) -> dict:
        if method == 'SPRING':
            positions = nx.spring_layout(self.graph, iterations=1000, weight=spectral_weight, dim=dimension, seed=1)

        elif method == 'KAMADA-KAWAI':
            positions = nx.kamada_kawai_layout(self.graph, dim = dimension)

        elif method == 'SPECTRAL':
            positions = nx.spectral_layout(self.graph, weight=spectral_weight)

        elif method == 'CIRCULAR':
            positions = nx.circular_layout(self.graph)

        elif method == 'RANDOM':
            positions = nx.random_layout(self.graph)
        
        elif method == 'SHELL':
            positions = nx.shell_layout(self.graph)

        else:
            positions = nx.kamada_kawai_layout(self.graph)

        return positions

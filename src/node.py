from src.edge import Edge

class Node:
    def __init__(self, unit):
        self.unit = unit
        self.edges = []

    def add_edge(self, multiplier, other_node):
        edge = Edge(multiplier=multiplier, node=other_node)
        self.edges.append(edge)
        
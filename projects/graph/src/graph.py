"""
Simple graph implementation
"""
from queue import Queue
from stack import Stack


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertices(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
            self.vertices[v2].add(v1)
        else:
            raise IndexError("That vertex does not exist")

    def add_directed_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist")

    def bft(self, starting_vertex_id, target_id):
        q = Queue()
        q.enqueue(starting_vertex_id)
        visited = set()
        while q.size() > 0:
            v = q.dequeue()
            print(v)
            visited.add(v)
            for next_vert in self.vertices[v]:
                q.enqueue(next_vert)

    def dft(self, starting_vertex_id):
        s = Stack()
        s.push(starting_vertex_id)
        visited = set()
        while s.size() > 0:
            v = s.pop()
            print(v)
            visited.add(v)
            for next_vert in self.vertices[v]:
                s.push(next_vert)

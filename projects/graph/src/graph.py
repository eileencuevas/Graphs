"""
Simple graph implementation
"""
from queue import Queue
from stack import Stack


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
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

    def bft(self, starting_vertex_id):  # Breath-First Traversal
        q = Queue()
        q.enqueue(starting_vertex_id)
        visited = set()
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                print(f"current vertex {v}")
                visited.add(v)
                for next_vert in self.vertices[v]:
                    q.enqueue(next_vert)

    def dft(self, starting_vertex_id):  # Depth-First Traversal
        s = Stack()
        s.push(starting_vertex_id)
        visited = set()
        while s.size() > 0:
            v = s.pop()
            if v not in visited:
                print(f"current vertex {v}")
                visited.add(v)
                for next_vert in self.vertices[v]:
                    s.push(next_vert)

    def dft_recursive(self, starting_vertex_id, visited=None):
        if visited is None:
            visited = set()
        if starting_vertex_id not in visited:
            visited.add(starting_vertex_id)
            print(f"current vertex: {starting_vertex_id}")
            for next_vert in self.vertices[starting_vertex_id]:
                self.dft_recursive(next_vert, visited)

    def bfs(self, starting_vertex, target):  # Breath-First Search
        search_queue = Queue()
        search_queue.enqueue([starting_vertex])
        visited = set()
        while search_queue.size() > 0:
            current_path = search_queue.dequeue()
            current_vertex = current_path[-1]
            if current_vertex not in visited:
                if current_vertex == target:
                    return current_path
                visited.add(current_vertex)
                for next_vert in self.vertices[current_vertex]:
                    new_path = list(current_path)
                    new_path.append(next_vert)
                    search_queue.enqueue(new_path)
        return f"No route found from {starting_vertex} to {target}"

    def dfs(self, starting_vertex, target):  # Depth-First Search
        search_stack = Stack()
        search_stack.push([starting_vertex])
        visited = set()
        while search_stack.size() > 0:
            current_path = search_stack.pop()
            current_vertex = current_path[-1]
            if current_vertex not in visited:
                if current_vertex == target:
                    return current_path
                visited.add(current_vertex)
                for next_vert in self.vertices[current_vertex]:
                    new_path = list(current_path)
                    new_path.append(next_vert)
                    search_stack.push(new_path)
        # target not found
        return f"No route found from {starting_vertex} to {target}"

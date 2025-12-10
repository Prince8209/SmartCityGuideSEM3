"""
Custom Graph Implementation
Used for: City connections, route planning, network analysis
"""

from .queue import Queue


class Graph:
    """
    Custom Graph implementation using adjacency list
    Supports both directed and undirected graphs
    Demonstrates: graph algorithms, BFS, DFS, Dijkstra
    """
    
    def __init__(self, directed=False):
        self.graph = {}  # Adjacency list: {vertex: {neighbor: weight}}
        self.directed = directed
    
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph
        Args:
            vertex: Vertex identifier (can be any hashable type)
        """
        if vertex not in self.graph:
            self.graph[vertex] = {}
    
    def add_edge(self, from_vertex, to_vertex, weight=1):
        """
        Add edge between vertices with optional weight
        Args:
            from_vertex: Starting vertex
            to_vertex: Ending vertex
            weight: Edge weight (default 1)
        """
        # Ensure vertices exist
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        
        # Add edge
        self.graph[from_vertex][to_vertex] = weight
        
        # If undirected, add reverse edge
        if not self.directed:
            self.graph[to_vertex][from_vertex] = weight
    
    def remove_edge(self, from_vertex, to_vertex):
        """Remove edge between vertices"""
        if from_vertex in self.graph and to_vertex in self.graph[from_vertex]:
            del self.graph[from_vertex][to_vertex]
            
            if not self.directed and from_vertex in self.graph[to_vertex]:
                del self.graph[to_vertex][from_vertex]
    
    def remove_vertex(self, vertex):
        """Remove vertex and all its edges"""
        if vertex not in self.graph:
            return
        
        # Remove all edges to this vertex
        for v in self.graph:
            if vertex in self.graph[v]:
                del self.graph[v][vertex]
        
        # Remove vertex
        del self.graph[vertex]
    
    def get_neighbors(self, vertex):
        """
        Get all neighbors of a vertex
        Returns: Dictionary of {neighbor: weight}
        """
        return self.graph.get(vertex, {})
    
    def has_edge(self, from_vertex, to_vertex):
        """Check if edge exists"""
        return (from_vertex in self.graph and 
                to_vertex in self.graph[from_vertex])
    
    def get_weight(self, from_vertex, to_vertex):
        """Get weight of edge"""
        if self.has_edge(from_vertex, to_vertex):
            return self.graph[from_vertex][to_vertex]
        return None
    
    def vertices(self):
        """Return list of all vertices"""
        return list(self.graph.keys())
    
    def edges(self):
        """Return list of all edges as (from, to, weight) tuples"""
        edges = []
        for from_v in self.graph:
            for to_v, weight in self.graph[from_v].items():
                if self.directed or (to_v, from_v, weight) not in edges:
                    edges.append((from_v, to_v, weight))
        return edges
    
    def bfs(self, start):
        """
        Breadth-First Search traversal
        Demonstrates: queue usage, graph traversal
        Returns: List of vertices in BFS order
        """
        if start not in self.graph:
            return []
        
        visited = set()
        queue = Queue()
        queue.enqueue(start)
        visited.add(start)
        result = []
        
        while not queue.is_empty():
            vertex = queue.dequeue()
            result.append(vertex)
            
            # Visit all neighbors
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
        
        return result
    
    def dfs(self, start):
        """
        Depth-First Search traversal
        Demonstrates: recursion, graph traversal
        Returns: List of vertices in DFS order
        """
        if start not in self.graph:
            return []
        
        visited = set()
        result = []
        
        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result
    
    def dijkstra(self, start):
        """
        Dijkstra's shortest path algorithm
        Demonstrates: greedy algorithm, priority queue concept
        Returns: Dictionary of {vertex: shortest_distance_from_start}
        """
        if start not in self.graph:
            return {}
        
        # Initialize distances
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        visited = set()
        
        while len(visited) < len(self.graph):
            # Find unvisited vertex with minimum distance
            current = None
            min_dist = float('inf')
            
            for vertex in self.graph:
                if vertex not in visited and distances[vertex] < min_dist:
                    min_dist = distances[vertex]
                    current = vertex
            
            if current is None:
                break
            
            visited.add(current)
            
            # Update distances to neighbors
            for neighbor, weight in self.graph[current].items():
                distance = distances[current] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
        
        return distances
    
    def shortest_path(self, start, end):
        """
        Find shortest path between two vertices using Dijkstra
        Returns: (path, distance) tuple
        """
        if start not in self.graph or end not in self.graph:
            return None, float('inf')
        
        # Track distances and previous vertices
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        previous = {vertex: None for vertex in self.graph}
        visited = set()
        
        while len(visited) < len(self.graph):
            # Find unvisited vertex with minimum distance
            current = None
            min_dist = float('inf')
            
            for vertex in self.graph:
                if vertex not in visited and distances[vertex] < min_dist:
                    min_dist = distances[vertex]
                    current = vertex
            
            if current is None or current == end:
                break
            
            visited.add(current)
            
            # Update distances and track path
            for neighbor, weight in self.graph[current].items():
                distance = distances[current] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
        
        # Reconstruct path
        if distances[end] == float('inf'):
            return None, float('inf')
        
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        return path, distances[end]
    
    def is_connected(self):
        """Check if graph is connected (for undirected graphs)"""
        if not self.graph:
            return True
        
        start = next(iter(self.graph))
        visited = set(self.bfs(start))
        
        return len(visited) == len(self.graph)
    
    def has_cycle(self):
        """Check if graph has a cycle"""
        visited = set()
        rec_stack = set()
        
        def has_cycle_util(vertex, parent=None):
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor, vertex):
                        return True
                elif neighbor in rec_stack:
                    if self.directed or neighbor != parent:
                        return True
            
            rec_stack.remove(vertex)
            return False
        
        for vertex in self.graph:
            if vertex not in visited:
                if has_cycle_util(vertex):
                    return True
        
        return False
    
    def __len__(self):
        """Return number of vertices"""
        return len(self.graph)
    
    def __contains__(self, vertex):
        """Check if vertex exists"""
        return vertex in self.graph
    
    def __repr__(self):
        return f"Graph(vertices={len(self.graph)}, directed={self.directed})"
    
    def __str__(self):
        """User-friendly string representation"""
        lines = [f"Graph (directed={self.directed}):"]
        for vertex in sorted(self.graph.keys()):
            neighbors = ", ".join(
                f"{n}({w})" for n, w in self.graph[vertex].items()
            )
            lines.append(f"  {vertex} -> {neighbors if neighbors else 'None'}")
        return "\n".join(lines)

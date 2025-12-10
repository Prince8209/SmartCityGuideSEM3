"""
Route Optimizer Service
Uses Graph and NumPy for route optimization
"""

import numpy as np
from app.data_structures.graph import Graph


class RouteOptimizer:
    """
    Optimize travel routes using Graph + NumPy
    Demonstrates: graph algorithms, NumPy calculations
    """
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Haversine formula using NumPy
        Demonstrates: NumPy trigonometric functions
        """
        R = 6371  # Earth radius in km
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c
    
    @staticmethod
    def optimize_route(cities):
        """
        Optimize route using greedy nearest neighbor
        Demonstrates: NumPy matrix operations, algorithms
        """
        if not cities or len(cities) <= 2:
            return {
                'cities': cities,
                'total_distance': 0,
                'route_order': list(range(len(cities)))
            }
        
        n = len(cities)
        
        # Create distance matrix using NumPy
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distances[i][j] = RouteOptimizer.calculate_distance(
                        cities[i]['latitude'],
                        cities[i]['longitude'],
                        cities[j]['latitude'],
                        cities[j]['longitude']
                    )
        
        # Greedy nearest neighbor algorithm
        visited = np.zeros(n, dtype=bool)
        route = [0]
        visited[0] = True
        total_distance = 0
        
        for _ in range(n - 1):
            last = route[-1]
            
            # Find nearest unvisited city
            unvisited_distances = distances[last].copy()
            unvisited_distances[visited] = np.inf
            
            nearest = np.argmin(unvisited_distances)
            
            route.append(nearest)
            visited[nearest] = True
            total_distance += distances[last][nearest]
        
        # Reorder cities according to route
        optimized_cities = [cities[i] for i in route]
        
        return {
            'cities': optimized_cities,
            'total_distance': round(total_distance, 2),
            'route_order': route,
            'distance_matrix': distances.tolist()
        }

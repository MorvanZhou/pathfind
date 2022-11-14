from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import PriorityFrontier
from pathfind.graph.graph import Node


class Dijkstra(BaseFinder):
    def __init__(self):
        super().__init__(PriorityFrontier())

    def check_neighbors(self, current: Node):
        for neighbor, cost in self.neighbors(current):
            new_cost = self.cost_to(current) + cost
            if not self.in_cost_record(neighbor) or new_cost < self.cost_to(neighbor):
                self.reset_cost_to(neighbor, new_cost)
                self.frontier.put(neighbor, new_cost)
                self.came_from[neighbor.name] = current

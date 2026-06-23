import heapq

class Pathfinder:
    VALUES = {
        "restricted": 2,
        "normal": 1,
        "priority": 1,
        "blocked": float("inf")
    }

    def __init__(self, start_hub, end_hub, hubs, connections):
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = hubs
        self.connections = connections

    def find_shortest_paths(self, position):
        self._setup_graph_values()
        paths = []
        neighbors = {}
        current_path = []
        stack = [position.name]
        while stack:
            neighbors[stack[0].name] = self._get_connected(stack[0])
            stack.extend(neighbors[stack[0].name].keys())
            heapq.heapify(neighbors[stack[0].name])
            heapq.heappop()

    def _setup_graph_values(self):
        self.values = {}
        try:
            self.end_hub.zone
        except AttributeError:
            self.values[self.end_hub[0]] = 1
        else:
            self.values[self.end_hub[0]] = self.VALUES[self.end_hub.zone]
        for hub_name in self.hubs.keys():
            try:
                self.hubs[hub_name].zone
            except AttributeError:
                self.values[hub_name] = 1
            else:
                self.values[hub_name] = (
                    self.VALUES[self.hubs[hub_name].zone])

    def _get_connected(self, current):
        connected = []
        for connection in current.connections:
            if current == connection.hubs[0] and connection.hubs[1] in self.values:
                connected.append((self.values[connection.hubs[1].name], connection.hubs[1].name))
            elif current == connection.hubs[1] and connection.hubs[0].name in self.values:
                connected.append((self.values[connection.hubs[1].name], connection.hubs[1].name))
        return connected

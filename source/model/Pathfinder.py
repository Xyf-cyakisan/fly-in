class Pathfinder:
    VALUES = {
        "restricted": 2,
        "normal": 1,
        "priority": float("-inf"),
        "blocked": float("inf")
    }

    def __init__(self, start_hub, end_hub, hubs, connections):
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = hubs
        self.connections = connections

    def find_shortest_path(self, og_position,  to_avoid):
        self._setup_graph_values(to_avoid)
        fastest_paths = {hub.name: [float("inf"), []] for hub in list(self.hubs.values()) + [self.end_hub, self.start_hub]}
        queue = [(0, og_position, [])]
        current_path = []
        while queue:
            current = queue.pop()
            current_path = current[2]
            if current[0] > fastest_paths[current[1].name][0]:
                continue
            else:
                neighbors = self._get_neighbors_of_hub(current[1], current_path)
                for neighbor in neighbors:
                    distance = 1 if current[0] == float("-inf") and self.values[neighbor.name] == float("inf") else current[0]  + 1 if self.values[neighbor.name] == float("-inf") and current[0] == float("inf") else self.values[neighbor.name]
                    if distance < fastest_paths[neighbor.name][0]:
                        queue.append((distance, neighbor, current_path + [neighbor]))
                        fastest_paths[neighbor.name] = (distance, current_path + [neighbor])
        return fastest_paths[self.end_hub.name][1]

    def _get_neighbors_of_hub(self, hub, current_path):
        neighbors = []
        for connection in hub.connections:
            neighbor = connection.hubs[0] if hub == connection.hubs[1] else connection.hubs[1]
            if neighbor not in current_path:
                neighbors.append(neighbor)
        return neighbors

    def _setup_graph_values(self, to_avoid):
        self.values = {self.start_hub.name: 1}
        try:
            self.end_hub.zone
        except AttributeError:
            self.values[self.end_hub.name] = 1
        else:
            self.values[self.end_hub.name] = self.VALUES[self.end_hub.zone]
        for hub_name in self.hubs.keys():
            try:
                self.hubs[hub_name].zone
            except AttributeError:
                self.values[hub_name] = 1
            else:
                self.values[hub_name] = (
                    self.VALUES[self.hubs[hub_name].zone])
        for hub in to_avoid:
            self.values[hub.name] = self.VALUES["blocked"]

    def _get_connected(self, current, path):
        connected = []
        for connection in current.connections:
            if current == connection.hubs[0] and connection.hubs[1].name in self.values.keys() and connection.hubs[1] not in path:
                connected.append((self.values[connection.hubs[1].name], connection.hubs[1]))
            elif current == connection.hubs[1] and connection.hubs[0].name in self.values.keys() and connection.hubs[0] not in path:
                connected.append((self.values[connection.hubs[0].name], connection.hubs[0]))
        return connected

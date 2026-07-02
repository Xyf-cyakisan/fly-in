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

    def find_shortest_path(self, og_position, to_avoid):
        self._setup_graph_values(to_avoid)
        path = []
        neighbors = {og_position: self._get_connected(og_position, path)}
        current = (0, og_position)
        if neighbors[og_position] == []:
            return None
        while neighbors[og_position] != [] or current[1] != og_position:
            try:
                neighbors[current[1]]
            except KeyError:
                neighbors[current[1]] = self._get_connected(current[1], path)
            if neighbors[current[1]] != []:
                if self.end_hub in [neighbor[1] for neighbor in neighbors[current[1]]]:
                    path.append(self.end_hub)
                    break
                if len({neighbor[0] for neighbor in neighbors[current[1]]}) > 1:
                    only_cost = [neighbor[0] for neighbor in neighbors[current[1]]]
                    previous = current
                    current = neighbors[current[1]][only_cost.index(min(only_cost))]
                    neighbors[previous[1]].pop(only_cost.index(min(only_cost)))
                else:
                    current = neighbors[current[1]].pop()
                path.append(current[1])
            else:
                if path != []:
                    path.pop()
                current = (self.values[path[-1].name], path[-1]) if path != [] else (0, og_position)
        if self.end_hub not in path:
            return None
        return path

    def _setup_graph_values(self, to_avoid):
        self.values = {}
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
            self.values.pop(hub.name)

    def _get_connected(self, current, path):
        connected = []
        for connection in current.connections:
            if current == connection.hubs[0] and connection.hubs[1].name in self.values.keys() and connection.hubs[1] not in path:
                connected.append((self.values[connection.hubs[1].name], connection.hubs[1]))
            elif current == connection.hubs[1] and connection.hubs[0].name in self.values.keys() and connection.hubs[0] not in path:
                connected.append((self.values[connection.hubs[0].name], connection.hubs[0]))
        return connected

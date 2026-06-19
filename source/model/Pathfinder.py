class Pathfinder:
    VALUES = {
        "restricted": 2,
        "normal": 1,
        "priority": float("-inf"),
        "blocked": None
    }

    def __init__(self, start_hub, end_hub, hubs, connections):
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = hubs
        self.connections = connections

    def find_shortest_paths(self, position):
        self._setup_graph_values()

    def _setup_graph_values(self):
        values = {}
        try:
            self.end_hub.zone
        except AttributeError:
            values[self.end_hub[0]] = 1
        else:
            values[self.end_hub[0]] = self.VALUES[self.end_hub.zone]
        for hub_name in self.hubs.keys():
            try:
                self.hubs[hub_name].zone
            except AttributeError:
                values[self.hubs[hub_name][0]] = 1
            else:
                values[self.hubs[hub_name][0]] = self.VALUES[self.hubs[hub_name].zone]

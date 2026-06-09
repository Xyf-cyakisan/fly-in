from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from ..parser.MapConfig import MapConfig
from .Pathfinder import Pathfinder

class Graph:
    def __init__(self, map_config: MapConfig, pathfinder : Pathfinder):
        self.start_hub = Hub(map_config.start_hub, map_config.metadata["start_hub"])
        self.end_hub = Hub(map_config.end_hub, map_config.metadata["end_hub"])
        self.hubs = {}
        for hub in map_config.hub:
            self.hubs[hub[0]] = Hub(hub, map_config.metadata[hub[0]])
        self.connections = []
        for connection in map_config.connection:
            self.connections.append(Connection((self.hubs[connection[0]], self.hubs[connection[1]]), map_config.metadata[connection[0] + '-' + connection[1]]))
            self.hubs[connection[0]].setup_connection(self.connections[-1])
            self.hubs[connection[1]].setup_connection(self.connections[-1])
        self.drones = []
        for i in range(map_config.nb_drones):
            drone = Drone(i + 1, self.start_hub)
            self.drones.append(drone)
            self.start_hub.drones.append(drone)
        self.pathfinder = Pathfinder(self.zones, self.connections)
            

    def run_simulation(self):
        
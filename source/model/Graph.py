from ..utils import MovementError
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from ..parser.MapConfig import MapConfig
from .Pathfinder import Pathfinder


class Graph:
    def __init__(self, map_config: MapConfig):
        self.start_hub = Hub(map_config.start_hub, map_config.metadata[map_config.start_hub[0]])
        self.end_hub = Hub(map_config.end_hub, map_config.metadata[map_config.end_hub[0]])
        self.hubs = {}
        for hub in map_config.hub:
            self.hubs[hub[0]] = Hub(hub, map_config.metadata[hub[0]])
        self.connections = []
        for connection in map_config.connection:
            if connection[0] not in (self.start_hub.name, self.end_hub.name) and connection[1] not in (self.start_hub.name, self.end_hub.name):
                self.connections.append(Connection((self.hubs[connection[0]], self.hubs[connection[1]]), map_config.metadata[connection[0] + '-' + connection[1]]))
                self.hubs[connection[0]].setup_connection(self.connections[-1])
                self.hubs[connection[1]].setup_connection(self.connections[-1])
            else:
                if connection[0] in self.start_hub.name :
                    self.connections.append(Connection((self.start_hub, self.hubs[connection[1]]), map_config.metadata[connection[0] + '-' + connection[1]]))
                    self.start_hub.setup_connection(self.connections[-1])
                    self.hubs[connection[1]].setup_connection(self.connections[-1])
                elif connection[0] in self.end_hub.name:
                    self.connections.append(Connection((self.end_hub, self.hubs[connection[1]]), map_config.metadata[connection[0] + '-' + connection[1]]))
                    self.end_hub.setup_connection(self.connections[-1])
                    self.hubs[connection[1]].setup_connection(self.connections[-1])
                elif connection[1] in self.start_hub.name:
                    self.connections.append(Connection((self.hubs[connection[0]], self.start_hub), map_config.metadata[connection[0] + '-' + connection[1]]))
                    self.start_hub.setup_connection(self.connections[-1])
                    self.hubs[connection[0]].setup_connection(self.connections[-1])
                else:
                    self.connections.append(Connection((self.hubs[connection[0]], self.end_hub), map_config.metadata[connection[0] + '-' + connection[1]]))
                    self.end_hub.setup_connection(self.connections[-1])
                    self.hubs[connection[0]].setup_connection(self.connections[-1])
        self.drones = []
        for id in range(map_config.nb_drones):
            drone = Drone(id + 1, self.start_hub)
            self.drones.append(drone)
            self.start_hub.drones.append(drone)

    def _set_pathfinder(self):
        self.pathfinder = Pathfinder(self.start_hub, self.end_hub, self.hubs, self.connections)

    def _set_drones_path(self):
        for drone in self.drones:
            drone.set_path(self.pathfinder.find_shortest_path(drone.place))

    def run_simulation(self):
        self._set_pathfinder()
        self.pathfinder.check_if_possible_map()
        self._set_drones_path()
        for drone in self.drones:
            print(drone.place.name)

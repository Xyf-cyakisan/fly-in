from ..utils.MovementError import MovementError
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
                if connection[0] == self.start_hub.name and connection[1] == self.end_hub.name or connection[0] == self.end_hub.name and connection[1] == self.start_hub.name:
                    hubs = (self.start_hub, self.end_hub)
                elif connection[0] == self.start_hub.name:
                    hubs = (self.start_hub, self.hubs[connection[1]])
                elif connection[0] == self.end_hub.name:
                    hubs = (self.end_hub, self.hubs[connection[1]])
                elif connection[1] == self.start_hub.name:
                    hubs = (self.start_hub, self.hubs[connection[0]])
                elif connection[1] == self.end_hub.name:
                    hubs = (self.end_hub, self.hubs[connection[0]])
                self.connections.append(Connection(hubs, map_config.metadata[connection[0] + '-' + connection[1]]))
                hubs[0].setup_connection(self.connections[-1])
                hubs[1].setup_connection(self.connections[-1])
        self.drones = []
        for id in range(map_config.nb_drones):
            drone = Drone(id + 1, self.start_hub)
            self.drones.append(drone)
            self.start_hub.drones[id + 1] = drone
        self.turns = 0

    def _set_pathfinder(self):
        self.pathfinder = Pathfinder(self.start_hub, self.end_hub, self.hubs, self.connections)

    def _set_drones_path(self):
        for drone in self.drones:
            drone.set_path(self.pathfinder.find_shortest_path(drone.place, []))

    def run_simulation(self):
        tracks = {drone.id: [self.start_hub.name] for drone in self.drones}
        self._set_pathfinder()
        self._set_drones_path()
        i = 0
        while len(self.end_hub.drones) < len(self.drones):
            for drone in self.drones:
                if drone.place == self.end_hub:
                    tracks[drone.id].append("FINISHED")
                    continue
                else:
                    try:
                        tracks[drone.id].append(drone.move())
                    except MovementError:
                        to_avoid = {drone.path[0]}
                        path = self.pathfinder.find_shortest_path(drone.place, to_avoid)
                        drone.switch_path(path)
                        if path is not None and len(drone.path) + 1 < len(path):
                            to_avoid.add(path[0])
                        while True:
                            try:
                                tracks[drone.id].append(drone.move())
                            except MovementError:
                                to_avoid.add(drone.path[0])
                                path = self.pathfinder.find_shortest_path(drone.place, to_avoid)
                                drone.switch_path(path)
                                if path is not None and len(drone.path) + 1 < len(path):
                                    to_avoid.add(path[0])
                            else:
                                break
            for connection in self.connections:
                connection.reset()
            self.turns += 1
        for i in range(self.turns + 1):
            print(f"Turn {i}:")
            for drone in self.drones:
                print(f"drone_{drone.id}: " + tracks[drone.id][i])
        return tracks, self.turns

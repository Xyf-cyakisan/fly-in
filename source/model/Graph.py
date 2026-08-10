from ..utils.MovementError import MovementError
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from ..parser.MapConfig import MapConfig
from .Pathfinder import Pathfinder
from ..utils.simulation_funcs import get_path_len


class Graph:
    def __init__(self, map_config: MapConfig):
        self.start_hub = Hub(map_config.start_hub, map_config.metadata[map_config.start_hub[0]])
        self.end_hub = Hub(map_config.end_hub, map_config.metadata[map_config.end_hub[0]])
        self.hubs = {}
        for hub in map_config.hub:
            self.hubs[hub[0]] = Hub(hub, map_config.metadata[hub[0]])
        self.hubs.update({self.start_hub.name: self.start_hub,
                          self.end_hub.name: self.end_hub})
        self.connections = []
        for connection in map_config.connection:
            self.connections.append(Connection((self.hubs[connection[0]], self.hubs[connection[1]]), map_config.metadata[connection[0] + '-' + connection[1]]))
            self.hubs[connection[0]].setup_connection(self.connections[-1])
            self.hubs[connection[1]].setup_connection(self.connections[-1])
        self.drones = []
        for id in range(map_config.nb_drones):
            drone = Drone(id + 1, self.start_hub)
            self.drones.append(drone)
            self.start_hub.drones[id + 1] = drone
        self.turns = 0
        self.tracks = {drone.id: [] for drone in self.drones}
        self.capacity = [{place.name: f"{len(place.drones)}/{place.max_drones}" for place in list(self.hubs.values())}]

    def _set_pathfinder(self):
        self.pathfinder = Pathfinder(self.start_hub, self.end_hub, self.hubs, self.connections)

    def _set_drones_path(self):
        for drone in self.drones:
            drone.set_path(self.pathfinder.find_shortest_path(drone.place, []))

    def run_simulation(self):
        self._set_pathfinder()
        self._set_drones_path()
        while len(self.end_hub.drones) < len(self.drones):
            for drone in self.drones:
                if drone.place == self.end_hub:
                    self.tracks[drone.id].append(("", drone.place.name))
                    continue
                else:
                    try:
                        self.tracks[drone.id].append(drone.move())
                        self.tracks[drone.id][-1] = (self.tracks[drone.id][-1], drone.place.name)
                    except MovementError:
                        original_path = drone.path
                        to_avoid = {drone.path[0]}
                        if drone.previous_place is not None:
                            to_avoid.add(drone.previous_place)
                        path = self.pathfinder.find_shortest_path(drone.place, to_avoid)
                        if path != []:
                            if get_path_len(path) <= get_path_len(original_path) + 1:
                                drone.set_path(path)
                            else:
                                to_avoid.add(path[0])
                        if path == []:
                            drone.set_path(original_path)
                            self.tracks[drone.id].append(("", drone.place.name))
                        else:
                            while True:
                                try:
                                    self.tracks[drone.id].append(drone.move())
                                    self.tracks[drone.id][-1] = (self.tracks[drone.id][-1], drone.place.name)
                                except MovementError:
                                    to_avoid.add(drone.path[0])
                                    path = self.pathfinder.find_shortest_path(drone.place, to_avoid)
                                    if path == []:
                                        drone.set_path(original_path)
                                        self.tracks[drone.id].append(("", drone.place.name))
                                        break
                                    if get_path_len(path) <= get_path_len(original_path) + 1:
                                        drone.set_path(path)
                                    else:
                                        to_avoid.add(path[0])
                                else:
                                    break
            self.capacity.append({place.name: f"{len(place.drones)}/{place.max_drones}" for place in list(self.hubs.values())})
            for connection in self.connections:
                connection.reset()
            self.turns += 1
        for i in range(self.turns):
            print(f"Turn {i + 1}: ", end="")
            for drone in self.drones:
                print(self.tracks[drone.id][i][0], end=" " if self.tracks[drone.id][i][0] != "" else "")
            print()

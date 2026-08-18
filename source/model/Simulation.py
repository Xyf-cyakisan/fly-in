from ..utils.MovementError import MovementError
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from ..parser.MapConfig import MapConfig
from .Pathfinder import Pathfinder
from ..utils.simulation_funcs import get_path_len


class Simulation:
    def __init__(self, map_config: MapConfig):
        self.start_hub: Hub = Hub(map_config.start_hub,
                                  map_config.metadata[map_config.start_hub[0]])
        self.end_hub: Hub = Hub(map_config.end_hub,
                                map_config.metadata[map_config.end_hub[0]])
        self.hubs: dict[str, Hub] = {}
        for hub in map_config.hub:
            self.hubs[hub[0]] = Hub(hub, map_config.metadata[hub[0]])
        self.hubs.update({self.start_hub.name: self.start_hub,
                          self.end_hub.name: self.end_hub})
        self.connections: list[Connection] = []
        for connection in map_config.connection:
            self.connections.append(Connection((self.hubs[connection[0]],
                                                self.hubs[connection[1]]),
                                               map_config.metadata[connection[
                                                    0] + '-' + connection[1]]))
            self.hubs[connection[0]].setup_connection(self.connections[-1])
            self.hubs[connection[1]].setup_connection(self.connections[-1])
        self.drones: list[Drone] = []
        for id in range(map_config.nb_drones):
            drone = Drone(id + 1, self.start_hub)
            self.drones.append(drone)
            self.start_hub.drones[id + 1] = drone
        self.pathfinder: Pathfinder = Pathfinder(self.start_hub,
                                                 self.end_hub, self.hubs,
                                                 self.connections)
        self.turns: int = 0
        self.tracks: dict[int, list[tuple[str, str] | str]] = {drone.id: [] for
                                                               drone in
                                                               self.drones}
        self.capacity: list[dict[str, str]] = [{
            place.name: f"{len(place.drones)}/{getattr(place, "max_drones",
                                                       1)}"
                        for place in list(self.hubs.values())}]

    def _set_drones_path(self) -> None:
        for drone in self.drones:
            drone.set_path(self.pathfinder.find_shortest_path(self.start_hub,
                                                              set()))

    def _switch_path_trial_and_error(self, drone: Drone) -> None:
        original_path = drone.path
        to_avoid = {drone.path[0]}
        if drone.previous_place is not None:
            to_avoid.add(drone.previous_place)
        if isinstance(drone.place, Hub):
            path = self.pathfinder.find_shortest_path(
                drone.place, to_avoid)
        if path != []:
            if (get_path_len(path) <=
               get_path_len(original_path) + 1):
                drone.set_path(path)
            else:
                to_avoid.add(path[0])
        if path == []:
            drone.set_path(original_path)
            self.tracks[drone.id].append(("", drone.place.name)
                                         )
        else:
            while True:
                try:
                    move = drone.move()
                    self.tracks[drone.id].append(
                        (move, drone.place.name))
                except MovementError:
                    to_avoid.add(drone.path[0])
                    if isinstance(drone.place, Hub):
                        path = (
                            self.pathfinder.find_shortest_path(
                                drone.place, to_avoid))
                    if path == []:
                        drone.set_path(original_path)
                        self.tracks[drone.id].append(
                            ("", drone.place.name))
                        break
                    if (get_path_len(path)
                       <= get_path_len(original_path) + 1):
                        drone.set_path(path)
                    else:
                        to_avoid.add(path[0])
                else:
                    break

    def run_simulation(self) -> None:
        self._set_drones_path()
        while len(self.end_hub.drones) < len(self.drones):
            for drone in self.drones:
                if drone.place == self.end_hub:
                    self.tracks[drone.id].append(("", drone.place.name))
                    continue
                else:
                    try:
                        move = drone.move()
                        self.tracks[drone.id].append((move, drone.place.name))
                    except MovementError:
                        self._switch_path_trial_and_error(drone)
            self.capacity.append(
                {place.name: f"{len(place.drones)}/{getattr(place,
                                                            "max_drones", 1)}"
                 for place in list(self.hubs.values())})
            for connection in self.connections:
                connection.reset()
            self.turns += 1

from ..utils.MovementError import MovementError
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from ..parser.MapConfig import MapConfig
from .Pathfinder import Pathfinder
from ..utils.simulation_funcs import get_path_len


class Simulation:
    def __init__(self, map_config: MapConfig):
        self.__start_hub: Hub = Hub(
            map_config.start_hub, map_config.metadata[map_config.start_hub[0]]
        )
        self.__end_hub: Hub = Hub(
            map_config.end_hub, map_config.metadata[map_config.end_hub[0]]
        )
        self.__hubs: dict[str, Hub] = {}
        for hub in map_config.hub:
            self.__hubs[hub[0]] = Hub(hub, map_config.metadata[hub[0]])
        self.__hubs.update(
            {
                self.__start_hub.get_name(): self.__start_hub,
                self.__end_hub.get_name(): self.__end_hub,
            }
        )
        self.__connections: list[Connection] = []
        for connection in map_config.connection:
            self.__connections.append(
                Connection(
                    (self.__hubs[connection[0]], self.__hubs[connection[1]]),
                    map_config.metadata[connection[0] + "-" + connection[1]],
                )
            )
            self.__hubs[connection[0]].setup_connection(self.__connections[-1])
            self.__hubs[connection[1]].setup_connection(self.__connections[-1])
        self.__drones: list[Drone] = []
        for id in range(map_config.nb_drones):
            drone = Drone(id + 1, self.__start_hub)
            self.__drones.append(drone)
            self.__start_hub.add_drone(id + 1, drone)
        self.__pathfinder: Pathfinder = Pathfinder(
            self.__end_hub, self.__hubs
        )
        self.__tracks: dict[int, list[tuple[str, str] | str]] = {
            drone.get_id(): [] for drone in self.__drones
        }
        self.__capacity: dict[str, list[str]] = {
            place.get_name(): [
                f"{len(place.get_drones())}/{getattr(place, 'max_drones', 1)}"
            ]
            for place in self.__hubs.values()
        }

    def get_start_hub(self) -> Hub:
        return self.__start_hub

    def get_hubs(self) -> dict[str, Hub]:
        return self.__hubs

    def get_connections(self) -> list[Connection]:
        return self.__connections

    def get_len_drones(self) -> int:
        return len(self.__drones)

    def get_tracks(self) -> dict[int, list[tuple[str, str] | str]]:
        return self.__tracks

    def get_capacity(self) -> dict[str, list[str]]:
        return self.__capacity

    def _set_drones_path(self) -> None:
        for drone in self.__drones:
            drone.set_path(
                self.__pathfinder.find_shortest_path(self.__start_hub, set())
            )

    def _switch_path_trial_and_error(self, drone: Drone) -> None:
        original_path = drone.get_path()
        to_avoid = {drone.get_path()[0]}
        previous_place = drone.get_previous_place()
        if isinstance(previous_place, Hub):
            to_avoid.add(previous_place)
        drone_place = drone.get_place()
        if isinstance(drone_place, Hub):
            path = self.__pathfinder.find_shortest_path(drone_place,
                                                        to_avoid)
        if path != []:
            if get_path_len(path) <= get_path_len(original_path) + 1:
                drone.set_path(path)
            else:
                to_avoid.add(path[0])
        if path == []:
            drone.set_path(original_path)
            self.__tracks[drone.get_id()].append(("",
                                                  drone.get_place().get_name())
                                                 )
        else:
            while True:
                try:
                    move = drone.move()
                    self.__tracks[
                        drone.get_id()].append((move,
                                                drone.get_place().get_name()))
                except MovementError:
                    to_avoid.add(drone.get_path()[0])
                    drone_place = drone.get_place()
                    if isinstance(drone_place, Hub):
                        path = self.__pathfinder.find_shortest_path(
                            drone_place, to_avoid
                        )
                    if path == []:
                        drone.set_path(original_path)
                        self.__tracks[drone.get_id()].append(("",
                                                              drone.get_place(
                                                              ).get_name()))
                        break
                    if get_path_len(path) <= get_path_len(original_path) + 1:
                        drone.set_path(path)
                    else:
                        to_avoid.add(path[0])
                else:
                    break

    def _update_capacity(self) -> None:
        for key in self.__capacity.keys():
            place = self.__hubs[key]
            self.__capacity[key].append(
                f"{len(place.get_drones())}/{getattr(place, 'max_drones', 1)}"
            )

    def run_simulation(self) -> None:
        self._set_drones_path()
        while len(self.__end_hub.get_drones()) < len(self.__drones):
            for drone in self.__drones:
                if drone.get_place() == self.__end_hub:
                    self.__tracks[drone.get_id()].append(("",
                                                          drone.get_place(
                                                          ).get_name()))
                    continue
                else:
                    try:
                        move = drone.move()
                        self.__tracks[drone.get_id()
                                      ].append(
                                          (move, drone.get_place().get_name()))
                    except MovementError:
                        self._switch_path_trial_and_error(drone)
            self._update_capacity()
            for connection in self.__connections:
                connection.reset()

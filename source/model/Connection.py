from ..utils.MovementError import MovementError
from .Hub import Hub
from ..utils.simulation_funcs import check_restricted_connections


class Connection:
    def __init__(self, hubs: tuple[Hub, Hub], max_link_capacity):
        self.name = hubs[0].name + "-" + hubs[1].name
        self.hubs = list(hubs)
        self.max_link_capacity = max_link_capacity["max_link_capacity"]
        self.drones = {}
        self.passed_through = 0

    def _get_destination(self, drone_zone):
        if drone_zone.name == self.hubs[0].name:
            try:
                self.hubs[1].zone
            except AttributeError:
                return self.hubs[1]
            else:
                if self.hubs[1].zone == "restricted":
                    return self
                else:
                    return self.hubs[1]
        elif drone_zone.name == self.hubs[1].name:
            try:
                self.hubs[0].zone
            except AttributeError:
                return self.hubs[0]
            else:
                if self.hubs[0].zone == "restricted":
                    return self
                else:
                    return self.hubs[0]
        else:
            raise ValueError(f"Error: {drone_zone.name} is not "
                             "any of the two linked "
                             "connections ("
                             f"{self.hubs[0].name, self.hubs[1].name}).")

    def _destination_accessible(self, drone):
        if self.passed_through == self.max_link_capacity:
            return False
        zone = self._get_destination(drone.place)
        max_drones = (zone.max_drones
                      if isinstance(zone, Hub) else zone.max_link_capacity)
        nb_drones = len(zone.drones)
        if not isinstance(zone, Connection):
            if max_drones > nb_drones:
                return True
            else:
                return False
        else:
            restricted_hub = (zone.hubs[0]
                              if drone.place == zone.hubs[1] else zone.hubs[1])
            if (check_restricted_connections(restricted_hub)
                    == restricted_hub.max_drones):
                return False
            else:
                return True

    def drone_passing_through(self, drone):
        if self._destination_accessible(drone) is False:
            raise MovementError
        else:
            self._get_destination(drone.place).drone_arrival(drone)
            self.passed_through += 1

    def reset(self):
        self.passed_through = len(self.drones)

    def drone_arrival(self, drone) -> None:
        self.drones[drone.id] = drone
        drone.place = self

    def drone_departure(self, drone_id: int) -> None:
        self.drones[drone_id].path[0].drone_arrival(self.drones[drone_id])
        self.drones.pop(drone_id)

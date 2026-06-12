from ..utils.MovementError import MovementError

from .Hub import Hub


class Connection:
    def __init__(self, hubs: tuple[Hub, Hub], max_link_capacity):
        self.hubs = list(hubs)
        self.max_link_capacity = max_link_capacity
        self.drones = []
        self.passed_through = 0

    def _get_destination(self, drone_zone):
        if drone_zone.name == self.hubs[0].name:
            return self.hubs[1]
        elif drone_zone.name == self.hubs[1].name:
            return self.hubs[0]
        else:
            raise ValueError("Error: drone_zone is not any of the two linked "
                             "connections.")

    def _destination_accessible(self, drone_zone):
        if (self.max_link_capacity is not None and
           self.self.passed_through == self.max_link_capacity):
            return False
        try:
            zone = self._get_destination(drone_zone)
            max_drones = zone.max_drones
            nb_drones = len(zone.drones)
        except AttributeError:
            return True
        else:
            if max_drones == nb_drones:
                return False
            else:
                return True

    def drone_passing_through(self, drone):
        if not self._destination_accessible(drone.place):
            raise MovementError("Error: this connection is not accessible")
        else:
            self.passed_through += 1
            self._get_destination(drone.place).drone_arrival(drone)

    def reset(self):
        self.passed_through = len(self.drones)

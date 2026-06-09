from ..utils.MovementError import MovementError

from .Hub import Hub


class Connection:
    def __init__(self, zones: tuple[Hub, Hub], max_link_capacity=None):
        self.zones = list(zones)
        self.max_link_capacity = max_link_capacity
        self.drones = []

    def _get_destination(self, drone_zone):
        if drone_zone == self.zones[0].name:
            return self.zones[1]
        elif drone_zone == self.zones[1].name:
            return self.zones[0]
        else:
            raise ValueError("Error: drone_zone is not any of the two linked "
                             "connections.")

    def _destination_accessible(self, drone_zone):
        if (self.max_link_capacity is not None and
           len(self.drones) == self.max_link_capacity):
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
            self._get_destination(drone.place).drone_arrival(drone)


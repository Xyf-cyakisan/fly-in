from . import Zone


class Connection:
    def __init__(self, zones: tuple[Zone, Zone], max_link_capacity=None):
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

    def _accessible(self, drone_zone):
        if (self.max_link_capacity is not None and
           len(self.drones) == self.max_link_capacity or
           drone_zone not in self.zones):
            return False
        else:
            return True

    def drone_passing_through(self, drone):
        if not self._accessible(drone.place.name):
            raise ValueError("Error: this connection is not accessible")
        else:
            self._get_destination(drone.place).drone_arrival(drone)

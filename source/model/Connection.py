class Connection:
    def __init__(self, zones: tuple[str, str], max_link_capacity=None):
        self.zones = zones
        self.max_link_capacity = max_link_capacity
        self.drones = []

    def accessible(self, drone_zone):
        if (self.max_link_capacity is not None and
           self.drones == self.max_link_capacity or
           drone_zone not in self.zones):
            return False
        else:
            return True

    def drone_entering(self, drone):
        if not self.accessible(drone.place):
            raise ValueError("Error: this connection is not accessible")
        else:
            self.drones.append((drone, self._get_destination(drone.place)))

    def _get_destination(self, drone_zone):
        if self.zones[0] == drone_zone:
            return self.zones[1]
        else:
            return self.zones[0]

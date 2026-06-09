from ..utils.MovementError import MovementError


class Hub:
    def __init__(self, primary_data, metadata):
        self.drones = []
        self.name = primary_data[0]
        self.coordinates + (primary_data[1], primary_data[2])
        if metadata is not None:
            for key, value in metadata.items():
                setattr(self, key, value)
        self.connections = []

    def setup_connection(self, connection):
        self.connections.append(connection)

    def drone_arrival(self, drone):
        try:
            self.max_drones
        except AttributeError:
            self.drones.append(drone)
        else:
            if self.max_drones == len(self.drones):
                raise MovementError(f"Error: zone ({self.name}) cannot take "
                                 "another drone")
            else:
                self.drones.append(drone)

    def _get_connection(self, drone):
        for i, connection in enumerate(self.connections):
            if drone.path[0] in connection.zones:
                return i
        return False

    def drone_departure(self):
        for drone in self.drones:
            connection = self._get_connection(drone)
            if connection:
                self.connections[connection].drone_passing_through(drone)
            else:
                raise MovementError(f"Error: {drone.id} cannot go to {drone.path[0]}")

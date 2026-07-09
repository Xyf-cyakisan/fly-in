from ..utils.MovementError import MovementError


class Hub:
    def __init__(self, primary_data, metadata):
        self.drones = {}
        self.name = primary_data[0]
        self.coordinates = (primary_data[1], primary_data[2])
        if metadata is not None:
            for key, value in metadata.items():
                setattr(self, key, value)
        self.connections = []

    def setup_connection(self, connection):
        self.connections.append(connection)

    def drone_arrival(self, drone) -> None:
        try:
            self.zone
        except AttributeError:
            ...
        else:
            if self.zone == "blocked":
                raise MovementError
        try:
            self.max_drones
        except AttributeError:
            self.drones[drone.id] = drone
        else:
            if self.max_drones == len(self.drones):
                raise MovementError
            else:
                self.drones[drone.id] = drone
        drone.path.pop(0)
        drone.place = self

    def _get_connection(self, drone):
        for i, connection in enumerate(self.connections):
            if drone.path[0] in connection.hubs:
                return i
        return False

    def drone_departure(self, drone_id: int) -> None:
        drone = self.drones[drone_id]
        connection = self._get_connection(drone)
        if connection is not False:
            self.connections[connection].drone_passing_through(drone)
            self.drones.pop(drone_id)
        else:
            raise ValueError(f"Error: drone {drone.id} cannot go to "
                             f"{drone.path[0].name} from {self.name}")

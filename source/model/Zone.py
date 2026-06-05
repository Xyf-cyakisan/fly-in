class Zone:
    def __init__(self, primary_data, metadata):
        self.drones = []
        self.name = primary_data[0]
        self.coordinates + (primary_data[1], primary_data[2])
        if metadata is not None:
            for key, value in metadata.items():
                setattr(self, key, value)

    def setup_connections(self, connections):
        self.connections = connections

    def drone_arrival(self, drone):
        try:
            self.max_drones
        except AttributeError:
            self.drones.append(drone)
        else:
            if self.max_drones == len(self.drones):
                raise ValueError(f"Error: zone ({self.name}) cannot take "
                                 "another drone")
            else:
                self.drones.append(drone)

    def verify_destination(self, destination_name):
        found = False
        for connection in self.connections:
            if destination_name in connection.zones:
                
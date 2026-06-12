class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place = start_hub

    def set_path(self, path):
        self.path = path

    def move(self):
        self.place.drone_departure(self.id)

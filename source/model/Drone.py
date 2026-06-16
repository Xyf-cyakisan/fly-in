from .Place import Place


class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place: Place = start_hub

    def set_path(self, path):
        self.path = path

    def move(self) -> str:
        og_place = self.place.name
        try:
            self.path[0].restricted
        except AttributeError:
            move = og_place + '-' + self.path[0].name
        else:
            move = "Waiting in connection(" + og_place + '-' + self.path[0].name + ")"
        self.place.drone_departure(self.id)
        return move

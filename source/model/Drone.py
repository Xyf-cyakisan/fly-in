from ..model.Connection import Connection
from .Place import Place


class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place: Place = start_hub
        self.old_paths = []

    def set_path(self, path):
        self.old_paths = path
        self.path = path

    def move(self) -> str:
        og_place = self.place.name
        if self.path == []:
            self.set_path(self.old_paths)
            return f"WAITING ({self.place})"
        try:
            self.path[0].restricted
        except AttributeError:
            move = og_place + '-' + self.path[0].name
        else:
            move = "Waiting in connection(" + og_place + '-' + self.path[0].name + ")"
            if isinstance(self.place, Connection):
                move = og_place + '-' + self.path[0].name
        self.place.drone_departure(self.id)
        return move

    def switch_path(self):
        self.path.pop(0)

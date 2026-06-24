from .Connection import Connection
from .Place import Place


class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place: Place = start_hub
        self.old_paths = []
        self.path = None

    def set_path(self, path):
        if self.path is None or path is not None and len(self.path) + 1 >= len(path):
            self.path = path
        if path is None:
            self.path = ["WAITING"] + self.path

    def move(self) -> str:
        og_place = self.place.name
        if self.path[0] == "WAITING":
            self.path.pop(0)
            return f"WAITING ({self.place.name})"
        try:
            self.path[0].restricted
        except AttributeError:
            move = og_place + '-' + self.path[0].name
        else:
            move = "Waiting in connection(" + self.path[0] + '-' + self.path[0].name + ")"
            if isinstance(self.place, Connection):
                move = og_place + '-' + self.path[0].name
        self.place.drone_departure(self.id)
        return move

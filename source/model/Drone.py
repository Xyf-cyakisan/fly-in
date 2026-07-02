from .Connection import Connection
from .Place import Place


class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place: Place = start_hub
        self.path = None

    def set_path(self, path):
        self.path = path

    def switch_path(self, path):
        if path is not None and len(self.path) + 1 >= len(path):
            self.path = path
        elif path is None:
            self.path = ["WAITING"] + self.path

    def move(self) -> str:
        movement = self._get_move()
        if self.path[0] == "WAITING":
            self.path.pop(0)
            return movement
        self.place.drone_departure(self.id)
        return movement

    def _get_move(self):
        if self.path[0] == "WAITING":
            return "WAITING"
        if isinstance(self.place, Connection):
            return self.place.hubs[0].name + "-" + self.place.hubs[1].name if self.path[0].name == self.place.hubs[1].name else self.place.hubs[1].name + "-" + self.place.hubs[0].name
        else:
            try:
                self.path[0].zone
            except AttributeError:
                return self.place.name + "-" + self.path[0].name
            else:
                if self.path[0].zone == "restricted":
                    return "Waiting in connection (" + self.place.name + '-' + self.path[0].name + ")"
                else:
                    return self.place.name + "-" + self.path[0].name
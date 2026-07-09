from .Connection import Connection
from .Place import Place


class Drone:
    def __init__(self, d_id, start_hub):
        self.id = d_id
        self.place: Place = start_hub
        self.path = None
        self.previous_place = None

    def set_path(self, path):
        self.path = path

    def move(self) -> str:
        previous_place = self.place if not isinstance(self.place, Connection) else self.previous_place
        movement = self._get_move()
        self.place.drone_departure(self.id)
        self.previous_place = previous_place
        return movement

    def _get_move(self):
        if isinstance(self.place, Connection):
            return f"D{self.id}-" + self.place.hubs[1].name if self.path[0].name == self.place.hubs[1].name else self.place.hubs[0].name
        else:
            try:
                self.path[0].zone
            except AttributeError:
                return f"D{self.id}-" + self.path[0].name
            else:
                if self.path[0].zone == "restricted":
                    return f"D{self.id}-" + self.place.name + '-' + self.path[0].name
                else:
                    return f"D{self.id}-" + self.path[0].name

    def check_priority_in_path(self):
        for hub in self.path:
            try:
                hub.zone
            except AttributeError:
                continue
            else:
                if hub.zone == "priority":
                    return True
        return False

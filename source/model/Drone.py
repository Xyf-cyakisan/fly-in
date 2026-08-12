from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Hub import Hub
    from .Place import Place


class Drone:
    def __init__(self, d_id: int, start_hub: Hub) -> None:
        self.id = d_id
        self.place: Place = start_hub
        self.path = None
        self.previous_place = None

    def set_path(self, path: list[Hub]) -> None:
        self.path = path

    def move(self) -> str:
        previous_place = (
            self.place if self.place.place_type != "connection"
            else self.previous_place
        )
        movement = self._get_move()
        self.place.drone_departure(self.id)
        self.previous_place = previous_place
        return movement

    def _get_move(self) -> str:
        from ..model.Connection import Connection
        if isinstance(self.place, Connection):
            return (
                f"D{self.id}-" + self.place.hubs[1].name
                if self.path[0].name == self.place.hubs[1].name
                else self.place.hubs[0].name
            )
        else:
            try:
                self.path[0].type
            except AttributeError:
                return f"D{self.id}-" + self.path[0].name
            else:
                if self.path[0].type == "restricted":
                    return (
                        f"D{self.id}-"
                        + self.place.name
                        + "-"
                        + self.path[0].name
                    )
                else:
                    return f"D{self.id}-" + self.path[0].name

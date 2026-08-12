from typing import Protocol
from ..model.Drone import Drone


class Place(Protocol):
    place_type: str
    name: str

    def drone_arrival(self, drone: Drone) -> None:
        ...

    def drone_departure(self, drone_id: int) -> None:
        ...

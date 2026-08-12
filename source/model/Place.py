from typing import Protocol
from ..model.Drone import Drone


class Place(Protocol):
    def drone_arrival(self, drone: Drone) -> None:
        ...

    def drone_departure(self, drone_id: int) -> None:
        ...

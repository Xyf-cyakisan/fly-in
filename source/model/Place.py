from typing import Protocol
from ..model.Drone import Drone


class Place(Protocol):
    name: str
    drones: dict[int, Drone]

    def drone_arrival(self, drone: Drone) -> None:
        ...

    def drone_departure(self, drone_id: int) -> None:
        ...

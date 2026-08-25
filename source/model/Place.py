from typing import Protocol
from ..model.Drone import Drone


class Place(Protocol):
    __name: str
    __drones: dict[int, Drone]

    def drone_arrival(self, drone: Drone) -> None:
        ...

    def drone_departure(self, drone_id: int) -> None:
        ...

    def get_name(self) -> str:
        ...

    def get_drones(self) -> dict[int, Drone]:
        ...

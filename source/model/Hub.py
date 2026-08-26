from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Connection import Connection
from ..utils.MovementError import MovementError
from .Drone import Drone


class Hub:
    def __init__(
        self,
        primary_data: tuple[str, int, int],
        metadata: dict[str, str | int | None] | None,
    ) -> None:
        self.__drones: dict[int, Drone] = {}
        self.__name: str = primary_data[0]
        self.__coordinates: tuple[int, int] = (primary_data[1],
                                               primary_data[2])
        if metadata is not None:
            for key, value in metadata.items():
                if key == "zone":
                    key = "type"
                setattr(self, key, value)
        self.__connections: list[Connection] = []

    def add_drone(self, id: int, drone: Drone) -> None:
        self.__drones[id] = drone

    def get_drones(self) -> dict[int, Drone]:
        return self.__drones

    def get_name(self) -> str:
        return self.__name

    def get_coordinates(self) -> tuple[int, int]:
        return self.__coordinates

    def get_connections(self) -> list[Connection]:
        return self.__connections

    def setup_connection(self, connection: Connection) -> None:
        self.__connections.append(connection)

    def drone_arrival(self, drone: Drone) -> None:
        type = getattr(self, "type", None)
        if type is None:
            ...
        else:
            if type == "blocked":
                raise MovementError
        max_drones = getattr(self, "max_drones", None)
        if max_drones == len(self.__drones):
            raise MovementError
        else:
            self.add_drone(drone.get_id(), drone)
        drone.pop_path()
        drone.set_place(self)

    def _get_connection(self, drone: Drone) -> bool | int:
        for i, connection in enumerate(self.__connections):
            if drone.get_path()[0] in connection.get_hubs():
                return i
        return False

    def drone_departure(self, drone_id: int) -> None:
        drone = self.__drones[drone_id]
        connection = self._get_connection(drone)
        if connection is not False:
            self.__connections[connection].drone_passing_through(drone)
            self.__drones.pop(drone_id)
        else:
            raise ValueError(
                f"Error: drone {drone.get_id()} cannot go to "
                f"{drone.get_path()[0].get_name()} from {self.__name}"
            )

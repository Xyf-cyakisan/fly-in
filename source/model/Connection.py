from __future__ import annotations
from typing import TYPE_CHECKING

from .Place import Place
if TYPE_CHECKING:
    from .Drone import Drone
from ..utils.MovementError import MovementError
from .Hub import Hub
from ..utils.simulation_funcs import check_restricted_connections


class Connection:
    def __init__(self, hubs: tuple[Hub, Hub],
                 max_link_capacity: dict[str, str | int | None] | None
                 ) -> None:
        self.__name: str = hubs[0].get_name() + "-" + hubs[1].get_name()
        self.__hubs: list[Hub] = list(hubs)
        self.__max_link_capacity: int | str | None = (max_link_capacity.get(
            "max_link_capacity") if max_link_capacity is not None else 1)
        self.__drones: dict[int, Drone] = {}
        self.__passed_through: int = 0

    def get_name(self) -> str:
        return self.__name

    def get_hubs(self) -> list[Hub]:
        return self.__hubs

    def get_max_link_capacity(self) -> int | str | None:
        return self.__max_link_capacity

    def get_drones(self) -> dict[int, Drone]:
        return self.__drones

    def get_passed_through(self) -> int:
        return self.__passed_through

    def _get_destination(self, drone_zone: Place) -> Place:
        if drone_zone.get_name() == self.__hubs[0].get_name():
            hub_type = getattr(self.__hubs[1], "type", None)
            if hub_type is None:
                return self.__hubs[1]
            else:
                if hub_type == "restricted":
                    return self
                else:
                    return self.__hubs[1]
        elif drone_zone.get_name() == self.__hubs[1].get_name():
            hub_type = getattr(self.__hubs[0], "type", None)
            if hub_type is None:
                return self.__hubs[0]
            else:
                if hub_type == "restricted":
                    return self
                else:
                    return self.__hubs[0]
        else:
            raise ValueError(
                f"Error: {drone_zone.get_name()} is not "
                "any of the two linked "
                "connections ("
                f"{self.__hubs[0].get_name(), self.__hubs[1].get_name()})."
            )

    def _destination_accessible(self, drone: Drone) -> bool:
        if self.__passed_through == self.__max_link_capacity:
            return False
        zone = self._get_destination(drone.get_place())
        max_drones = (
            getattr(zone, "max_drones", 1)
            if isinstance(zone, Hub)
            else getattr(zone, "max_link_capacity", 1)
            if isinstance(zone, Connection) else 1)
        nb_drones = len(zone.get_drones())
        if not isinstance(zone, Connection):
            if max_drones > nb_drones:
                return True
            else:
                return False
        else:
            restricted_hub = (
                zone.get_hubs()[0] if drone.get_place() == zone.get_hubs()[1]
                else zone.get_hubs()[1]
            )
            if (
                check_restricted_connections(restricted_hub)
                == getattr(restricted_hub, "max_drones", 1)
            ):
                return False
            else:
                return True

    def drone_passing_through(self, drone: Drone) -> None:
        if self._destination_accessible(drone) is False:
            raise MovementError
        else:
            self._get_destination(drone.get_place()).drone_arrival(drone)
            self.__passed_through += 1

    def reset(self) -> None:
        self.__passed_through = len(self.__drones)

    def drone_arrival(self, drone: Drone) -> None:
        self.__drones[drone.get_id()] = drone
        drone.set_place(self)

    def drone_departure(self, drone_id: int) -> None:
        self.__drones[drone_id].get_path()[0].drone_arrival(self.__drones[
            drone_id])
        self.__drones.pop(drone_id)

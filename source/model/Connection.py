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
                 max_link_capacity: dict[str, int]) -> None:
        self.name: str = hubs[0].name + "-" + hubs[1].name
        self.hubs: list[Hub] = list(hubs)
        self.max_link_capacity: int = max_link_capacity["max_link_capacity"]
        self.drones: dict[int, Drone] = {}
        self.passed_through: int = 0
        self.place_type: str = "connection"

    def _get_destination(self, drone_zone: Place) -> Place:
        if drone_zone.name == self.hubs[0].name:
            hub_type = getattr(self.hubs[1], "type", None)
            if hub_type is None:
                return self.hubs[1]
            else:
                if hub_type == "restricted":
                    return self
                else:
                    return self.hubs[1]
        elif drone_zone.name == self.hubs[1].name:
            hub_type = getattr(self.hubs[0], "type", None)
            if hub_type is None:
                return self.hubs[0]
            else:
                if hub_type == "restricted":
                    return self
                else:
                    return self.hubs[0]
        else:
            raise ValueError(
                f"Error: {drone_zone.name} is not "
                "any of the two linked "
                "connections ("
                f"{self.hubs[0].name, self.hubs[1].name})."
            )

    def _destination_accessible(self, drone: Drone) -> bool:
        if self.passed_through == self.max_link_capacity:
            return False
        zone = self._get_destination(drone.place)
        max_drones = (
            getattr(zone, "max_drones", 1)
            if isinstance(zone, Hub)
            else getattr(zone, "max_link_capacity", 1)
            if isinstance(zone, Connection) else 1)
        nb_drones = len(zone.drones)
        if not isinstance(zone, Connection):
            if max_drones > nb_drones:
                return True
            else:
                return False
        else:
            restricted_hub = (
                zone.hubs[0] if drone.place == zone.hubs[1] else zone.hubs[1]
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
            self._get_destination(drone.place).drone_arrival(drone)
            self.passed_through += 1

    def reset(self) -> None:
        self.passed_through = len(self.drones)

    def drone_arrival(self, drone: Drone) -> None:
        self.drones[drone.id] = drone
        drone.place = self

    def drone_departure(self, drone_id: int) -> None:
        self.drones[drone_id].path[0].drone_arrival(self.drones[drone_id])
        self.drones.pop(drone_id)

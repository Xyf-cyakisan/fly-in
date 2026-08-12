from __future__ import annotations
from typing import TYPE_CHECKING
from ..model.Place import Place
if TYPE_CHECKING:
    from ..model.Hub import Hub


def get_path_len(path: list[Place]) -> int:
    counter = 0
    for hub in path:
        hub_type = getattr(hub, "type", None)
        if hub_type is None:
            counter += 1
        else:
            if hub_type == "restricted":
                counter += 2
            else:
                counter += 1
    return counter


def check_restricted_connections(restricted_hub: Hub) -> int:
    counter = 0
    for connection in restricted_hub.connections:
        counter += sum(
            [
                1
                for drone in connection.drones.values()
                if drone.previous_place != restricted_hub
            ]
        )
    return counter

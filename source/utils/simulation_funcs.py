from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..model.Hub import Hub


def get_path_len(path: list[Hub]) -> int:
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
    counter = len(restricted_hub.get_drones())
    for connection in restricted_hub.get_connections():
        counter += sum(
            [
                1
                for drone in connection.get_drones().values()
                if drone.get_previous_place() != restricted_hub
            ]
        )
    return counter

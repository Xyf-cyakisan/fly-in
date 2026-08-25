from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Hub import Hub
    from .Place import Place


class Drone:
    def __init__(self, d_id: int, start_hub: Hub) -> None:
        self.__id: int = d_id
        self.__place: Place = start_hub
        self.__previous_place: None | Hub = None

    def set_place(self, place: Place) -> None:
        self.__place = place

    def pop_path(self) -> None:
        self.__path.pop(0)

    def get_id(self) -> int:
        return self.__id

    def get_place(self) -> Place:
        return self.__place

    def get_previous_place(self) -> None | Hub:
        return self.__previous_place

    def set_path(self, path: list[Hub]) -> None:
        self.__path: list[Hub] = path

    def get_path(self) -> list[Hub]:
        return self.__path

    def move(self) -> str:
        from .Hub import Hub

        previous_place = (
            self.__place if isinstance(self.__place, Hub)
            else self.__previous_place
        )
        movement = self._get_move()
        self.__place.drone_departure(self.__id)
        self.__previous_place = previous_place
        return movement

    def _get_move(self) -> str:
        from ..model.Connection import Connection

        if isinstance(self.__place, Connection):
            return (
                f"D{self.__id}-" + self.__place.get_hubs()[1].get_name()
                if self.__path[0].get_name() == self.__place.get_hubs(
                )[1].get_name()
                else self.__place.get_hubs()[0].get_name()
            )
        else:
            next_hub_type = getattr(self.__path[0], "type", None)
            if next_hub_type is None:
                return f"D{self.__id}-" + self.__path[0].get_name()
            else:
                if next_hub_type == "restricted":
                    return (
                        f"D{self.__id}-"
                        + self.__place.get_name()
                        + "-"
                        + self.__path[0].get_name()
                    )
                else:
                    return f"D{self.__id}-" + self.__path[0].get_name()

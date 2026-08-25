from .Hub import Hub


class Pathfinder:
    TYPE_VALUES: dict[str, float] = {
        "restricted": 2.0,
        "normal": 1.0,
        "priority": 1.0,
        "blocked": float("inf"),
    }

    def __init__(
        self,
        end_hub: Hub,
        hubs: dict[str, Hub],
    ) -> None:
        self.__end_hub: Hub = end_hub
        self.__hubs: dict[str, Hub] = hubs

    def find_shortest_path(
        self, og_position: Hub, to_avoid: set[Hub]
    ) -> list[Hub]:
        self._setup_Simulation_values()
        fastest_paths: dict[str, tuple[float, list[Hub]]] = {
            hub.get_name(): (float("inf"), []) for hub in list(
                self.__hubs.values())
        }
        queue: list[tuple[float, Hub, list[Hub]]] = [(0, og_position, [])]
        current_path = []
        while queue:
            cheapest = self._get_cheapest(queue)
            current = queue[cheapest]
            current_path = current[2]
            queue.pop(cheapest)
            if current[0] > fastest_paths[current[1].get_name()][0]:
                continue
            else:
                neighbors = self._get_neighbors_of_hub(
                    current[1], current_path, to_avoid
                )
                for neighbor in neighbors:
                    distance = current[0] + self.values[neighbor.get_name()]
                    if (
                        distance < fastest_paths[neighbor.get_name()][0]
                        or distance == fastest_paths[neighbor.get_name()][0]
                        and self.check_priority_in_path(
                            fastest_paths[neighbor.get_name()][1]
                        )
                        is False
                        and self.check_priority_in_path(
                            current_path + [neighbor]
                        )
                        is True
                    ):
                        queue.append(
                            (distance, neighbor, current_path + [neighbor])
                        )
                        fastest_paths[neighbor.get_name()] = (
                            distance,
                            current_path + [neighbor],
                        )
        return fastest_paths[self.__end_hub.get_name()][1]

    def _get_neighbors_of_hub(
        self, hub: Hub, current_path: list[Hub], to_avoid: set[Hub]
    ) -> list[Hub]:
        neighbors = []
        if isinstance(hub, Hub):
            for connection in hub.get_connections():
                neighbor = (
                    connection.get_hubs()[0]
                    if hub == connection.get_hubs()[1]
                    else connection.get_hubs()[1]
                )
                if neighbor not in current_path and neighbor not in to_avoid:
                    neighbors.append(neighbor)
        return neighbors

    def check_priority_in_path(self, hubs: list[Hub]) -> bool:
        for hub in hubs:
            hub_type = getattr(hub, "type", None)
            if hub_type is None:
                continue
            else:
                if hub_type == "priority":
                    return True
        return False

    def _get_cheapest(self, queue: list[tuple[float, Hub, list[Hub]]]) -> int:
        if self.check_priority_in_path([hub[1] for hub in queue]):
            for _, hub, _ in queue:
                hub_type = getattr(hub, "type", None)
                if hub_type is None:
                    continue
                else:
                    if hub_type == "priority":
                        priorised = hub
                        break
            return [hub[1] for hub in queue].index(priorised)
        else:
            return [hub[0] for hub in queue].index(
                min([hub[0] for hub in queue])
            )

    def _setup_Simulation_values(self) -> None:
        self.values = {}
        for hub_name in self.__hubs.keys():
            hub_type = getattr(self.__hubs[hub_name], "type", None)
            if hub_type is None:
                self.values[hub_name] = 1.0
            else:
                self.values[hub_name] = self.TYPE_VALUES[hub_type]

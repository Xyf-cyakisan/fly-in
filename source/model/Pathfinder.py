from .Connection import Connection
from .Hub import Hub
from .Place import Place


class Pathfinder:
    TYPE_VALUES: dict[str, float] = {
        "restricted": 2.0,
        "normal": 1.0,
        "priority": 1.0,
        "blocked": float("inf"),
    }

    def __init__(
        self,
        start_hub: Hub,
        end_hub: Hub,
        hubs: dict[str, Hub],
        connections: list[Connection],
    ) -> None:
        self.start_hub: Hub = start_hub
        self.end_hub: Hub = end_hub
        self.hubs: dict[str, Hub] = hubs
        self.connections: list[Connection] = connections

    def find_shortest_path(self, og_position: Place, to_avoid: set[Place]
                           ) -> list[Place]:
        self._setup_graph_values()
        fastest_paths: dict[str, tuple[float, list[Place]]] = {
            hub.name: (float("inf"), []) for hub in list(self.hubs.values())
        }
        queue: list[tuple[float, Place, list[Place]]] = [(0, og_position, [])]
        current_path = []
        while queue:
            cheapest = self._get_cheapest(queue)
            current = queue[cheapest]
            current_path = current[2]
            queue.pop(cheapest)
            if current[0] > fastest_paths[current[1].name][0]:
                continue
            else:
                neighbors = self._get_neighbors_of_hub(
                    current[1], current_path, to_avoid
                )
                for neighbor in neighbors:
                    distance = current[0] + self.values[neighbor.name]
                    if (
                        distance < fastest_paths[neighbor.name][0]
                        or distance == fastest_paths[neighbor.name][0]
                        and self.check_priority_in_path(
                            fastest_paths[neighbor.name][1]
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
                        fastest_paths[neighbor.name] = (
                            distance,
                            current_path + [neighbor],
                        )
        return fastest_paths[self.end_hub.name][1]

    def _get_neighbors_of_hub(self, hub: Place, current_path: list[Place],
                              to_avoid: set[Place]) -> list[Hub]:
        neighbors = []
        if isinstance(hub, Hub):
            for connection in hub.connections:
                neighbor = (
                    connection.hubs[0]
                    if hub == connection.hubs[1]
                    else connection.hubs[1]
                )
                if neighbor not in current_path and neighbor not in to_avoid:
                    neighbors.append(neighbor)
        return neighbors

    def check_priority_in_path(self, hubs: list[Place]) -> bool:
        for hub in hubs:
            hub_type = getattr(hub, "type", None)
            if hub_type is None:
                continue
            else:
                if hub_type == "priority":
                    return True
        return False

    def _get_cheapest(self, queue: list[tuple[float, Place, list[Place]]]
                      ) -> int:
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

    def _setup_graph_values(self) -> None:
        self.values = {}
        for hub_name in self.hubs.keys():
            hub_type = getattr(self.hubs[hub_name], "type", None)
            if hub_type is None:
                self.values[hub_name] = 1.0
            else:
                self.values[hub_name] = self.TYPE_VALUES[hub_type]

from ..model.Simulation import Simulation
from ..parser.MapConfig import MapConfig
from ..render.Renderer import Renderer


class Controller:
    def __init__(self, map_config_file: str | None):
        self.map_config_file: str | None = map_config_file

    def __set_config(self) -> None:
        self.__map_config: MapConfig = MapConfig.parse(self.map_config_file)

    def __set_Simulation(self) -> None:
        self.__simulation: Simulation = Simulation(self.__map_config)

    def __set_view(self) -> None:
        self.__view: Renderer = Renderer(
            self.__simulation.get_len_drones(),
            self.__simulation.get_start_hub(),
            self.__simulation.get_hubs(),
            self.__simulation.get_connections(),
            self.__simulation.get_tracks(),
            self.__simulation.get_capacity()
        )

    def run(self) -> None:
        self.__set_config()
        self.__set_Simulation()
        self.__set_view()
        self.__simulation.run_simulation()
        self.__view.display_simulation()

from ..model.Graph import Graph
from ..parser.MapConfig import MapConfig


class Controller:
    def __init__(self, map_config_file: str):
        self.map_config_file = map_config_file

    def __set_config(self):
        self.__map_config = MapConfig.parse(self.map_config_file)

    def __set_graph(self):
        self.__graph = Graph(self.__map_config)

    def run(self):
        self.__set_config()
        self.__set_graph()
        self.__graph.run_simulation()

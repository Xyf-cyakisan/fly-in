from typing import Any


class MapConfig:

    COLORS = [
        "red",
        "blue",
        "yellow",
        "green",
        "orange",
        "purple",
        "cyan",
        "maroon",
        "brown",
        "lime",
        "magenta",
        "gold",
        "black",
        "darkred",
        "violet",
        "crimson",
        "rainbow"
    ]

    POSSIBLE_VALUES: list[str] = [
            "nb_drones",
            "start_hub",
            "hub",
            "end_hub",
            "connection",
    ]

    VALID_METADATA = {
        "hub": {
            "color": COLORS,
            "max_drones": None,
            "zone": [
                "restricted",
                "priority",
                "normal",
                "blocked"
            ]
        },
        "start_hub": {
            "color": COLORS,
            "max_drones": None
        },
        "end_hub": {
            "color": COLORS,
            "max_drones": None
        },
        "connection": {
            "max_link_capacity": None
        }
    }

    def __init__(self, nb_drones, start_hub, end_hub, hub, connection, metadata):
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hub = hub
        self.connection = connection
        self.metadata = metadata

    @classmethod
    def parse(cls, map_name: str) -> "MapConfig":
        content, lines = cls._read_file(map_name)
        raw_data = cls._convert_content_to_dict(content, lines)
        cls._all_data_types_covered(raw_data)
        raw_data = cls._convert_hubs_value_type(raw_data)
        raw_data = cls._convert_connections_value_type(raw_data)
        cls._check_hub_names(raw_data)
        cls._check_connections_duplicate(raw_data)
        cls._check_metadata_type(raw_data)
        cls._check_coordinates_duplicate(raw_data)
        raw_data.pop("lines")
        return cls(**raw_data)

    @staticmethod
    def _read_file(map_name: str) -> list[str]:
        content: list[str] = []
        lines = []
        with open(map_name, "r") as map:
            for i, line in enumerate(map):
                if line.startswith("#") or line == "\n":
                    continue
                else:
                    content.append(line.strip("\n"))
                    lines.append(i + 1)
        return content, lines

    @staticmethod
    def _check_mandatory_data(line: str, line_number: int) -> list[str]:
        list_data = line[1][:(line[1].find("[") if line[1].find("[") != -1 else len(line[1]))]
        list_data = [value for value in list_data.split(" ") if value != ""]
        if "hub" in line[0] and len(list_data) != 3:
            raise ValueError(f"Error (line {line_number}): {line[0]} must have 3 values (<name> <x> <y>)")
        elif "connection" in line[0]:
            if len(list_data) != 1:
                raise ValueError(f"Error (line {line_number}): {line[0]} must have 1 value (<zone_name1-zone_name2>)")
            list_data = list_data[0].split("-")
            if len(list_data) != 2:
                raise ValueError(f"Error (line {line_number}): {line[0]} must have 1 value (<zone_name1-zone_name2>)")
        elif "nb_drones" in line[0] and len(list_data) != 1:
            raise ValueError(f"Error (line {line_number}): {line[0]} must have 1 value (<non_zero_integer>)")
        return list_data

    @classmethod
    def _check_metadata(cls, line: list[str], line_number: int) -> dict[str, str] | None:
        brackets = (line[1].find("["), line[1].find("]"))
        if brackets[0] == -1 and brackets[1] == -1:
            return None
        if brackets[0] == -1 or brackets[1] == -1 or len(line[1]) > brackets[1] + 1:
            raise ValueError(f"Error (line {line_number}): metadata "
                             "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
        raw_metadata = line[1][brackets[0] + 1:brackets[1]]
        raw_metadata = [value for value in raw_metadata.split(" ") if value != ""]
        if raw_metadata == []:
            raise ValueError(f"Error (line {line_number}): metadata "
                             "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
        list_metadata = []
        for metadata in raw_metadata:
            splitted_metadata = metadata.split("=")
            if len(splitted_metadata) != 2:
                raise ValueError(f"Error (line {line_number}): metadata "
                                "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
            else:
                list_metadata.append(splitted_metadata)
        dict_metadata = {}
        for metadata in list_metadata:
            if line[0] not in cls.VALID_METADATA.keys() or metadata[0] not in cls.VALID_METADATA[line[0]].keys() or cls.VALID_METADATA[line[0]][metadata[0]] is not None and metadata[1] not in cls.VALID_METADATA[line[0]][metadata[0]]:
                if metadata[0] == "color" and len(metadata[1].split(" ")) == 1:
                    metadata[1] = "default"
                else:
                    raise ValueError(f"Error (line {line_number}): this metadata type is not possible ({metadata[0]}={metadata[1]})")
            dict_metadata[metadata[0]] = metadata[1]
        return dict_metadata

    @staticmethod
    def _check_hub_names(dict_content) -> None:
        names = []
        if '-' in dict_content["start_hub"][0]:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content["start_hub"][0]]}): name '{dict_content["start_hub"][0]}' should not have the '-' character in them")
        names.append(dict_content["start_hub"][0])
        if dict_content["end_hub"][0] in names:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content["end_hub"][0]]}): name '{dict_content["end_hub"][0]}' already exists")
        elif '-' in dict_content["end_hub"][0]:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content["end_hub"][0]]}): name '{dict_content["end_hub"][0]}' should not have the '-' character in them")
        names.append(dict_content["end_hub"][0])
        for name, _, _ in dict_content['hub']:
            if name in names:
                raise ValueError(f"Error (line {dict_content['lines'][name]}): name '{name}' already exists")
            elif '-' in name:
                raise ValueError(f"Error (line {dict_content['lines'][name]}): name '{name}' should not have the '-' character in them")
            names.append(name)
        for connection in dict_content["connection"]:
            if connection[0] not in names or connection[1] not in names:
                not_present = connection[0] if connection[0] not in names else connection[1] if connection[1] not in names else ""
                raise ValueError(f"Error (line {dict_content['lines'][connection[0] + '-' + connection[1]]}): '{not_present}' does not exists")

    @staticmethod
    def _check_connections_duplicate(dict_content) -> None:
        for i, connection_to_check in enumerate(dict_content['connection']):
            for y, connection in enumerate(dict_content['connection']):
                if i != y and set(connection) == set(connection_to_check):
                    raise ValueError(f"Error (line {dict_content["lines"][connection[0] + '-' + connection[1]]}): '{connection[0] + '-' + connection[1]}' this connection already exists")

    @classmethod
    def _all_data_types_covered(cls, dict_content) -> None:
        values_to_pass: dict[str, bool] = {
            "nb_drones": False,
            "start_hub": False,
            "hub": False,
            "end_hub": False,
            "connection": False,
        }
        for key in cls.POSSIBLE_VALUES:
            if dict_content.get(key, None):
                values_to_pass[key] = True
        not_passed: list[bool] = [key for key in values_to_pass.keys()
                                  if values_to_pass[key] is False]
        if not_passed != []:
            raise ValueError(f"Error: these value_type are missing "
                             f"{not_passed} in map file.")
        else:
            dict_content["start_hub"] = dict_content["start_hub"].pop()
            dict_content["end_hub"] = dict_content["end_hub"].pop()

    @staticmethod
    def _convert_hubs_value_type(dict_content) -> dict:
        try:
            dict_content["nb_drones"] = int(dict_content["nb_drones"])
            if dict_content["nb_drones"] <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(f"Error (line {dict_content['lines']['nb_drones']}): nb_drones needs to be a positive integer higher than 0")
        try:
            dict_content['start_hub'][1] = int(dict_content['start_hub'][1])
            dict_content['start_hub'][2] = int(dict_content['start_hub'][2])
            dict_content['start_hub'] = tuple(dict_content['start_hub'])
        except ValueError:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content['start_hub'][0]]}): coordinates x and y need to be integers")
        try:
            dict_content['end_hub'][1] = int(dict_content['end_hub'][1])
            dict_content['end_hub'][2] = int(dict_content['end_hub'][2])
            dict_content['end_hub'] = tuple(dict_content['end_hub'])
        except ValueError:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content['end_hub'][0]]}): coordinates x and y need to be integers")
        try:
            for i in range(len(dict_content['hub'])):
                dict_content['hub'][i][1] = int(dict_content['hub'][i][1])
                dict_content['hub'][i][2] = int(dict_content['hub'][i][2])
                dict_content['hub'][i] = tuple(dict_content['hub'][i])
        except ValueError:
            raise ValueError(f"Error (line {dict_content['lines'][dict_content['hub'][i][0]]}): coordinates x and y need to be integers")
        return dict_content

    @staticmethod
    def _convert_connections_value_type(dict_content) -> dict:
        for i in range(len(dict_content['connection'])):
            dict_content['connection'][i] = tuple(dict_content['connection'][i])
        return dict_content

    @classmethod
    def _convert_content_to_dict(cls, content: list[str], lines) -> dict[str, Any]:
        dict_content = {
            "nb_drones": None,
            "start_hub": [],
            "end_hub": [],
            "hub": [],
            "connection": [],
            "metadata": {},
            "lines": {}
        }
        if content[0].split(":")[0].strip(" ") != "nb_drones":
            raise ValueError("Error: first non-commentary and non-empty line must be nb_drones.")
        for i, line in zip(lines, content):
            if line.count(":") == 0:
                raise ValueError(
                    f"Error (line {i}): syntax is <value_type>: "
                    "<value> (depends on value_type) [metadata] "
                    "(depends on value_type)"
                )
            else:
                line = line.split(":")
                line[0].strip(" ")
                if len(line) != 2 or line[0] not in cls.POSSIBLE_VALUES:
                    raise ValueError(f"Error: (line {i}): value_type can "
                                     "ONLY be one of these parameters "
                                     f"{[cls.POSSIBLE_VALUES]} "
                                     "and syntax has to be like this: "
                                     "<value_type>:<value> (depends on"
                                     " value_type) [metadata] "
                                     "(depends on value_type)")
                else:
                    line_content = cls._check_mandatory_data(line, i)
                    metadata = cls._check_metadata(line, i)
                    if line[0] == "nb_drones":
                        dict_content["nb_drones"] = line_content[0]
                        dict_content["lines"]["nb_drones"] = i
                        dict_content["metadata"]["nb_drones"] = metadata

                    else:
                        type = line[0]
                        if line[0] not in "connection":
                            dict_content["metadata"][line_content[0]] = metadata
                            dict_content["lines"][line_content[0]] = i
                        else:
                            dict_content["metadata"][line_content[0] + "-" + line_content[1]] = metadata
                            dict_content["lines"][line_content[0] + "-" + line_content[1]] = i
                        dict_content[type].append(line_content)
                    if len(dict_content["start_hub"]) > 1 or len(dict_content["end_hub"]) > 1:
                        raise ValueError(f"Error (line {i}): Only 1 start_hub and end_hub")
        return dict_content

    def _check_metadata_type(dict_content) -> None:
        if dict_content['metadata'][dict_content['start_hub'][0]]:
            if isinstance(dict_content['metadata'][dict_content['start_hub'][0]], dict) and dict_content['metadata'][dict_content['start_hub'][0]].get("max_drones", None):
                try:
                    dict_content['metadata'][dict_content['start_hub'][0]]["max_drones"] = int(dict_content['metadata'][dict_content['start_hub'][0]]["max_drones"])
                except ValueError:
                    raise ValueError(f"Error (line {dict_content['lines'][dict_content['start_hub'][0]]}): max_drones for start_hub should be a positive integer")
        if dict_content['metadata'][dict_content['end_hub'][0]]:
            if isinstance(dict_content['metadata'][dict_content['end_hub'][0]], dict) and dict_content['metadata'][dict_content['end_hub'][0]].get("max_drones", None):
                try:
                    dict_content['metadata'][dict_content['end_hub'][0]]["max_drones"] = int(dict_content['metadata'][dict_content['end_hub'][0]]["max_drones"])
                except ValueError:
                    raise ValueError(f"Error (line {dict_content['lines'][dict_content['end_hub'][0]]}): max_drones for end_hub should be a positive integer")
        for hub in dict_content['hub']:
            if isinstance(dict_content['metadata'][hub[0]], dict) and dict_content['metadata'][hub[0]].get("max_drones", None):
                try:
                    dict_content['metadata'][hub[0]]["max_drones"] = int(dict_content['metadata'][hub[0]]["max_drones"])
                    if dict_content['metadata'][hub[0]]["max_drones"] <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {dict_content['lines'][hub[0]]}): max_drones for hub should be a positive integer higher than at least 0")
        for connection in dict_content['connection']:
            if isinstance(dict_content['metadata'][connection[0] + "-" + connection[1]], dict) and dict_content['metadata'][connection[0] + "-" + connection[1]].get("max_link_capacity", None):
                try:
                    dict_content['metadata'][connection[0] + "-" + connection[1]]["max_link_capacity"] = int(dict_content['metadata'][connection[0] + "-" + connection[1]]["max_link_capacity"])
                    if dict_content['metadata'][connection[0] + "-" + connection[1]]["max_link_capacity"] <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {dict_content['lines'][connection[0] + "-" + connection[1]]}): max_link_capacity for connection should be a positive integer higher than at least 0")

    def _check_coordinates_duplicate(dict_content) -> "MapConfig":
        if dict_content['start_hub'][1] == dict_content['end_hub'][1] and dict_content['start_hub'][2] == dict_content['end_hub'][2]:
            raise ValueError(f"Error (line {dict_content.lines[dict_content['end_hub'][0]]}): '{dict_content['end_hub'][0]}' is set at the same coordinates as '{dict_content['start_hub'][0]}'")
        for hub_to_check in dict_content['hub']:
            if hub_to_check[1] == dict_content['start_hub'][1] and hub_to_check[2] == dict_content['start_hub'][2]:
                raise ValueError(f"Error (line {dict_content.lines[hub_to_check[0]]}): '{hub_to_check[0]}' is set at the same coordinates as '{dict_content['start_hub'][0]}'")
            elif hub_to_check[1] == dict_content['end_hub'][1] and hub_to_check[2] == dict_content['end_hub'][2]:
                raise ValueError(f"Error (line {dict_content.lines[hub_to_check[0]]}): '{hub_to_check[0]}' is set at the same coordinates as '{dict_content['end_hub'][0]}'")
            for hub in dict_content['hub']:
                if hub_to_check[1] == hub[1] and hub_to_check[2] == hub[2] and hub[0] != hub_to_check[0]:
                    raise ValueError(f"Error (line {dict_content.lines[hub[0]]}): '{hub[0]}' is set at the same coordinates as '{hub_to_check[0]}'")
        return dict_content


if __name__ == "__main__":
    try:
        parsed = MapConfig.parse("maps/hard/01_maze_nightmare.txt")
    except Exception as e:
        print(e)
    else:
        print("START: ", parsed.start_hub, "metadata: ", parsed.metadata[parsed.start_hub[0]])
        print("end: ", parsed.end_hub, "metadata: ", parsed.metadata[parsed.end_hub[0]])
        print("drones: ", parsed.nb_drones, "metadata: ", parsed.metadata["nb_drones"])
        print()
        for hub in parsed.hub:
            print("hub:", hub[0], hub[1], hub[2], "metadata: ", parsed.metadata[hub[0]])
        print()
        for connection in parsed.connection:
            print("connection:", connection[0], connection[1], "metadata: ", parsed.metadata[connection[0] + "-" + connection[1]])
from typing import Any
import sys
try:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        model_validator,
        field_validator,
    )
except ImportError:
    print("\033c", end="")
    print("Errror: Pydantic not found.")
    sys.exit(1)

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


class MapConfig(BaseModel):
    nb_drones: int = Field(ge=1)
    start_hub: tuple[str, int, int]
    end_hub: tuple[str, int, int]
    hub: list[tuple[str, int, int]]
    connection: list[tuple[str, str]]
    metadata: dict[str, dict | None]
    lines: dict[str, int]

    @classmethod
    def parse(cls, map_name: str) -> "MapConfig":
        content, lines = cls._read_file(map_name)
        return cls(**(cls._convert_content_to_dict(content, lines)))

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

    @classmethod
    def _check_mandatory_data(cls, line: str, line_number: int) -> list[str]:
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
        brackets = (line[1].find("["), line[1].find("]"))
        if brackets[0] == -1 and brackets[1] == -1:
            return None
        if brackets[0] == -1 or brackets[1] == -1 or len(line[1]) > brackets[1] + 1:
            raise ValueError(f"Error (line {line_number}): metadata "
                             "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
        raw_metadata = line[1][brackets[0] + 1:brackets[1]]
        raw_metadata = [value for value in raw_metadata.split(" ") if value != ""]
        list_metadata = []
        for metadata in raw_metadata:
            if len(metadata.split("=")) % 2 != 0 or metadata.split("=") == -1:
                raise ValueError(f"Error (line {line_number}): metadata "
                                "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
            else:
                list_metadata.append(metadata.split("="))
        dict_metadata = {}
        for metadata in list_metadata:
            if line[0] not in VALID_METADATA.keys() or VALID_METADATA[line[0]][metadata[0]] is not None and metadata[1] not in VALID_METADATA[line[0]][metadata[0]]:
                raise ValueError(f"Error (line {line_number}): this metadata type is not possible ({metadata[0]}={metadata[1]})")
            
            dict_metadata[metadata[0]] = metadata[1]
        return dict_metadata

    @classmethod
    def _convert_content_to_dict(cls, content: list[str], lines) -> dict[str, Any]:
        values_to_pass: dict[str, bool] = {
            "nb_drones": False,
            "start_hub": False,
            "hub": False,
            "end_hub": False,
            "connection": False,
        }
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
            raise ValueError("Error: first non-commentary or non-empty line must be nb_drones.")
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
                if len(line) != 2 or line[0] not in values_to_pass.keys():
                    raise ValueError(f"Error: (line {i}): value_type can "
                                     "ONLY be one of these parameters "
                                     f"{[values_to_pass.keys()]} "
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
                    values_to_pass[line[0]] = True
                    if len(dict_content["start_hub"]) > 1 or len(dict_content["end_hub"]) > 1:
                        raise ValueError(f"Error (line {i}): Only 1 start_hub and end_hub")
        not_passed: list[bool] = [key for key in values_to_pass.keys()
                                  if values_to_pass[key] is False]
        if not_passed != []:
            raise ValueError(f"Error: these value_type are missing "
                             f"{not_passed} in map file.")
        dict_content["start_hub"] = dict_content["start_hub"].pop()
        dict_content["end_hub"] = dict_content["end_hub"].pop()
        return dict_content

    @model_validator(mode="after")
    def _check_metadata_type(self) -> "MapConfig":
        if self.metadata[self.start_hub[0]]:
            if isinstance(self.metadata[self.start_hub[0]], dict) and self.metadata[self.start_hub[0]].get("max_drones", None):
                try:
                    self.metadata[self.start_hub[0]]["max_drones"] = int(self.metadata[self.start_hub[0]]["max_drones"])
                    if self.metadata[self.start_hub[0]]["max_drones"] < self.nb_drones:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {self.lines[self.start_hub[0]]}): max_drones for start_hub should be a positive integer higher or equal to nb_drones")
        if self.metadata[self.end_hub[0]]:
            if isinstance(self.metadata[self.end_hub[0]], dict) and self.metadata[self.end_hub[0]].get("max_drones", None):
                try:
                    self.metadata[self.end_hub[0]]["max_drones"] = int(self.metadata[self.end_hub[0]]["max_drones"])
                    if self.metadata[self.end_hub[0]]["max_drones"] < self.nb_drones:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {self.lines[self.end_hub[0]]}): max_drones for end_hub should be a positive integer higher or equal to nb_drones")
        for hub in self.hub:
            if isinstance(self.metadata[hub[0]], dict) and self.metadata[hub[0]].get("max_drones", None):
                try:
                    self.metadata[hub[0]]["max_drones"] = int(self.metadata[hub[0]]["max_drones"])
                    if self.metadata[hub[0]]["max_drones"] <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {self.lines[hub[0]]}): max_drones for hub should be a positive integer higher or equal to nb_drones")
        for connection in self.connection:
            if isinstance(self.metadata[connection[0] + "-" + connection[1]], dict) and self.metadata[connection[0] + "-" + connection[1]].get("max_link_capacity", None):
                try:
                    self.metadata[connection[0] + "-" + connection[1]]["max_link_capacity"] = int(self.metadata[connection[0] + "-" + connection[1]]["max_link_capacity"])
                    if self.metadata[connection[0] + "-" + connection[1]]["max_link_capacity"] <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Error (line {self.lines[connection[0] + "-" + connection[1]]}): max_link_capacity for connection should be a positive integer higher or equal to nb_drones")
        return self


if __name__ == "__main__":
    try:
        parsed = MapConfig.parse("maps/hard/03_ultimate_challenge.txt")
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
from typing import Any
from pydantic import BaseModel, ValidationError, model_validator, Field


class Parser(BaseModel):
    nb_drones: int = Field(ge=1)

    VALID_METADATA = {
        "hub": {
            "color": [
                "red",
                "blue",
                "yellow",
                "green"
            ],
            "max_drones": None,
            "zone": [
                "restricited",
                "priority",
                "normal",
                "blocked"
            ]
        },
        "start_hub": {
            "color": [
                "red",
                "blue",
                "yellow",
                "green"
            ],
            "max_drones": None
        },
        "end_hub": {
            "color": [
                "red",
                "blue",
                "yellow",
                "green"
            ],
            "max_drones": None
        },
        "connection": {
            "max_link_capacity": None
        }
    }

    @classmethod
    def parse(cls, map_name: str) -> "Parser":
        try:
            content: list[str] = cls._read_file(map_name)
            return cls(**cls._convert_content_to_dict(content))
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except PermissionError as e:
            raise PermissionError(e)
        except ValueError as e:
            raise ValueError(e)

    @staticmethod
    def _read_file(map_name: str) -> list[str]:
        content: list[str] = []
        with open(map_name, "r") as map:
            for line in map:
                if line.startswith("#") or line == "":
                    continue
                else:
                    content.append(line)
        return content

    @staticmethod
    def _check_mandatory_data(line: str, line_number: int) -> list[str]:
    @classmethod
    def _check_metadata(cls, line: str, line_number: int) -> dict[str, str] | None:
        brackets = tuple(line[1].find("["), line[1].find("]"))
        if brackets[0] == -1 and brackets[1] == -1:
            return
        if brackets[0] == -1 or brackets[1] == -1 or len(line[1]) > brackets[1] + 1:
            raise ValueError(f"Error (line {line_number}): metadata "
                             "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
        raw_metadata = line[1][brackets[0] + 1:brackets[1]]
        raw_metadata = raw_metadata.split(" ")
        list_metadata = []
        for metadata in raw_metadata:
            if len(metadata.split("=")) % 2 != 0 or metadata.split("=") == -1:
                raise ValueError(f"Error (line {line_number}): metadata "
                                "syntax is [metadata1=value1 metadata2=value2] at the end of the line")
            else:
                list_metadata.append(metadata.split("="))
        dict_metadata = {}
        for metadata in list_metadata:
            if line[0] not in cls.VALID_METADATA.keys() or metadata[1] not in cls.VALID_METADATA[line[0]]:
                raise ValueError(f"Error (line {line_number}): this metadata type is not possible")
            
            dict_metadata[metadata[0]] = metadata[1]
        return dict_metadata

    @classmethod
    def _convert_content_to_dict(cls, content: list[str]) -> dict[str, Any]:
        values_to_pass: dict[str, bool] = {
            "nb_drones": False,
            "start_hub": False,
            "hub": False,
            "end_hub": False,
            "connection": False,
        }
        dict_content = {}
        for i, line in enumerate(content):
            if line.count(":") == 0:
                raise ValueError(
                    f"Error (line {i + 1}): syntax is <value_type>: "
                    "<value> (depends on value_type) [metadata] "
                    "(depends on value_type)"
                )
            else:
                line = line.split(":")
                if len(line) != 2 or line[0] not in values_to_pass.keys():
                    raise ValueError(f"Error: (line {i + 1}): value_type can "
                                     "ONLY be one of these parameters "
                                     f"{[values_to_pass.keys()]} "
                                     "and syntax has to be like this: "
                                     "<value_type>:<value> (depends on"
                                     " value_type) [metadata] "
                                     "(depends on value_type)")
                else:
                    cls._check_mandatory_data(line, i)
                    cls._check_metadata(line, i)
                    values_to_pass[line] = True
        not_passed: list[bool] = [key for key in values_to_pass.keys()
                                  if values_to_pass[key] is False]
        if not_passed == []:
            raise ValueError(f"Error: these value_type are missing "
                             f"{not_passed} in map file.")

    @staticmethod
    def _convert_content_to_dict(content: list[str]) -> dict[str, Any]:

import dataclasses
import json
import sys
from dataclasses import dataclass
from typing import Any


# a dict to compare the boundary values to the one set in config file
BOUNDS: dict[str, tuple[int, int]] = {
    "levels": (10, 100),
    "width": (14, 100),
    "height": (10, 100),
    "seed": (1, 1000)
}


@dataclass
class GameConfig:
    """Settings used by the game."""
    levels: int = 10
    width: int = 25
    height: int = 25
    seed: int = 42


class ConfigService:
    """Read and check the game settings."""
    def _read_file(self, file_path: str) -> str:
        """only read a file and return it as a text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
        except FileNotFoundError as e:
            print(f"Error: no config file provided: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        return data

    def _strip_comments(self, data: str) -> str:
        '''strip comments
        '''
        cleaned_data = []
        data_lst = data.splitlines()  # returns a list of lines
        for line in data_lst:
            tmp_line = line.lstrip()
            if tmp_line.startswith("#") or tmp_line.startswith("//"):
                cleaned_data.append("")
            else:
                cleaned_data.append(line)
        return "\n".join(cleaned_data)

    def _check_config(self, name: str, value: Any) -> bool:
        """Check that settings are valid."""
        if isinstance(value, bool) or not isinstance(value, int):
            return False
        bounds = BOUNDS.get(name)
        if bounds is None:
            return True
        low, high = bounds
        number = int(value)
        return low <= number <= high

    def load_config(self, file_path: str) -> GameConfig:
        """Read settings from a file."""
        data = self._read_file(file_path)
        cleaned_text = self._strip_comments(data)
        try:
            json_data = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            print(f"Invalid json format: {e}")
            sys.exit(1)
        if not isinstance(json_data, dict):
            print("incorrect format..")
            sys.exit(1)
        config = GameConfig()
        for field in dataclasses.fields(GameConfig):
            name = field.name
            if name not in json_data:
                print(f"the setting infos of: {name} aren't provided")
                # the defaults are already kept no need to reset them
                continue
            value = json_data[name]
            if self._check_config(name, value):
                setattr(config, field.name, value)
            else:
                print(f"invalid value provided for this setting: {name}")
        return config

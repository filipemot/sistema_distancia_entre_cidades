import json
import os
from typing import Any, Optional


class ConfigsService:
    data_config = None

    def __init__(self, folder: str, file_name: str) -> None:
        self.data_config = self.__read_file(folder, file_name)

    @staticmethod
    def __read_file(folder: str, file_name: str) -> Optional[Any]:
        configs: Optional[Any] = None
        file = os.path.join(folder, file_name)
        if os.path.exists(file):
            with open(file, encoding='utf-8') as json_data_file:
                configs = json.load(json_data_file)

        return configs

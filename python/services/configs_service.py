import json
import os
from typing import Dict, Any, Optional


class ConfigsService:
    data_config = None

    def __init__(self, folder: str, file_name: str) -> None:
        self.data_config = self.read_file(folder, file_name)

    @staticmethod
    def read_file(folder: str, file_name: str) -> Optional[Any]:
        configs: Optional[Any] = None
        file = os.path.join(folder, file_name)
        if os.path.exists(file):
            with open(file, encoding='utf-8') as json_data_file:
                configs = json.load(json_data_file)

        return configs

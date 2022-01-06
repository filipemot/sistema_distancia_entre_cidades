import json
import os


class ConfigsService:
    data_config = None

    def __init__(self, folder, file_name):
        self.data_config = self.read_file(folder, file_name)

    @staticmethod
    def read_file(folder, file_name):
        configs = None
        file = os.path.join(folder, file_name)
        if os.path.exists(file):
            with open(file, encoding='utf-8') as json_data_file:
                configs = json.load(json_data_file)

        return configs

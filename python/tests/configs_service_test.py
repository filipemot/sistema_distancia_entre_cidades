import os
import unittest

from arcgisscripting import ExecuteError  # type: ignore

from services.configs_service import ConfigsService


class TestConfigsService(unittest.TestCase):


    def test_configs_service_file_exists(self):
        self.configs_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config.json")

        assert self.configs_service.data_config is not None
        assert self.configs_service.data_config["workspace"] is not None
        assert self.configs_service.data_config["excel_city"] is not None
        assert self.configs_service.data_config["excel_states"] is not None
        assert self.configs_service.data_config["route"] is not None

    def test_configs_service_file_not_exists(self):
        self.configs_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config_Not_exists.json")

        assert self.configs_service.data_config is None

import os
import unittest

import pytest
from arcgisscripting import ExecuteError  # type: ignore

from services.config_db_service import ConfigDbService


class TestConfigsDbService(unittest.TestCase):

    def test_configs_db_service_file_exists(self):
        self.configs_service = ConfigDbService()
        db = self.configs_service.config(filename=os.path.dirname(os.path.abspath(__file__)) + "//database.ini")

        assert db is not None
        assert db["host"] is not None
        assert db["database"] is not None
        assert db["user"] is not None
        assert db["password"] is not None
        assert db["port"] is not None

    def test_configs_db_service_file_not_exists(self):
        with pytest.raises(Exception) as e:
            self.configs_service = ConfigDbService()
            db = self.configs_service.config(filename=os.path.dirname(os.path.abspath(__file__)) +
                                                      "\\database_not_exists.ini")

        assert e.value.args[0].index('Section postgresql not found in the') > -1


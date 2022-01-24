import unittest

from unittest import mock
from unittest.mock import Mock, patch

import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from models.city import City
from services.city_db_service import CityDbService

class MockStr:
    def __init__(self, data):
        self.data = data

    def decode(self, type_decode):
        return self.data


class MockCursorPsycopg2:
    method_access = ''

    def execute(self, sql) -> None:
        self.method_access = self.method_access + 'execute'
        pass

    def close(self) -> None:
        self.method_access = self.method_access + ',close'
        pass


class TestCityDbService(unittest.TestCase):

    @patch("services.city_db_service.CityDbService.__init__")
    def test_city_db_service_all_cities(self, spy_city_db_service_init):
        spy_city_db_service_init.return_value = None

        with mock.patch("services.db_services.DbService") as spy_db_service_init:
            spy_db_service_init.return_value = Mock()
            city_db_service = CityDbService()
            city_db_service.db_services = Mock()
            city_db_service.db_services.commit.return_value = True
            city_db_service.delete_all_cities()
        assert city_db_service.db_services is not None

    @patch("services.city_db_service.CityDbService.__init__")
    def test_city_db_service_insert_cities(self, spy_city_db_service_init):
        spy_city_db_service_init.return_value = None
        city = City('És', 1, 1, 1.0, 1.0, True, 'state', 1)
        list_cities = [city]

        city_db_service = CityDbService()

        with mock.patch.object(CityDbService, "_CityDbService__get_values_insert") as spy_get_values_insert:
            with mock.patch.object(CityDbService, "db_services") as spy_db_services:
                cursor = MockCursorPsycopg2()
                spy_get_values_insert.return_value = 'sql'
                spy_db_services.conn.cursor.return_value = cursor

                city_db_service.insert_cities(list_cities)
                spy_db_services.conn.cursor.assert_called_once()

                spy_db_services.commit.assert_called_once()
                assert spy_db_services.conn.cursor is not None
                assert cursor.method_access == 'execute,close'

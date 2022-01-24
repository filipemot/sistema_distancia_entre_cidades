import unittest

from unittest import mock
from unittest.mock import Mock
from mock import patch

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

    def mogrify(self, query, vars_str=None) -> MockStr:
        self.method_access = 'mogrify'
        return MockStr(str(vars_str))

    def execute(self, sql) -> None:
        self.method_access = self.method_access + ',execute'
        pass

    def close(self) -> None:
        pass


class MockPsycopg2:
    method_access = ''
    cursor_mock = MockCursorPsycopg2()

    def cursor(self) -> MockCursorPsycopg2:
        self.method_access = 'Cursor'
        return self.cursor_mock


class MockDbService:
    conn = MockPsycopg2()

    method_access = ''

    def commit(self) -> None:
        self.method_access = 'Commit'


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
        city_db_service.db_services = MockDbService()
        city_db_service.insert_cities(list_cities)

        assert city_db_service.db_services is not None
        assert city_db_service.db_services.method_access == 'Commit'
        assert city_db_service.db_services.conn.method_access == 'Cursor'
        assert city_db_service.db_services.conn.cursor_mock.method_access == 'mogrify,execute'

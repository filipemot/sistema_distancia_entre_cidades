import unittest

from unittest import mock
from unittest.mock import Mock, patch, call

import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from models.distance import Distance

from services.distance_db_service import DistanceDbService


class MockCursorPsycopg2:
    method_access = ''

    def execute(self, sql, parameters=None) -> None:
        self.method_access = self.method_access + 'execute'
        pass

    def close(self) -> None:
        self.method_access = self.method_access + ',close'
        pass


class TestDistanceDbService(unittest.TestCase):

    @patch("services.distance_db_service.DistanceDbService.__init__")
    def test_distance_db_service_delete_all_distances(self, spy_distance_db_service_init):
        spy_distance_db_service_init.return_value = None

        distance_db_service = DistanceDbService()
        with mock.patch.object(DistanceDbService, "db_services") as spy_db_services:
            cursor = MockCursorPsycopg2()
            spy_db_services.conn.cursor.return_value = cursor
            distance_db_service.delete_all_distances()
        spy_db_services.conn.cursor.assert_called_once()
        spy_db_services.commit.assert_called_once()
        assert spy_db_services.conn.cursor is not None

    @patch("services.distance_db_service.DistanceDbService.__init__")
    def test_distance_db_service_insert_distances(self, spy_distance_db_service_init):
        spy_distance_db_service_init.return_value = None
        distance = Distance(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

        distance_db_service = DistanceDbService()

        with mock.patch.object(DistanceDbService, "db_services") as spy_db_services:
            cursor = MockCursorPsycopg2()
            spy_db_services.conn.cursor.return_value = cursor
            distance_db_service.insert_distances(distance)

        spy_db_services.conn.cursor.assert_called_once()
        spy_db_services.commit.assert_called_once()
        assert spy_db_services.conn.cursor is not None
        assert cursor.method_access == 'execute,close'

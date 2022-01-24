import unittest

from unittest import mock
from unittest.mock import Mock, patch, call

import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from models.city import City
from models.distance import Distance
from services.city_db_service import CityDbService
from services.distance_db_service import DistanceDbService
from utils.constants import FIELD_DISTANCE_TABLE_POSTGREE, FIELD_DISTANCE_ID_POSTGREE, \
    FIELD_DISTANCE_ID_ORIGIN_POSTGREE, FIELD_DISTANCE_ID_DESTINATION_POSTGREE, FIELD_DISTANCE_MINUTES_POSTGREE, \
    FIELD_DISTANCE_TRAVEL_TIME_POSTGREE, FIELD_DISTANCE_MILES_POSTGREE, FIELD_DISTANCE_KILOMETER_POSTGREE, \
    FIELD_DISTANCE_TIME_AT_POSTGREE, FIELD_DISTANCE_WALK_TIME_POSTGREE, FIELD_DISTANCE_TRUCK_TIME_POSTGREE, \
    FIELD_DISTANCE_TRAVEL_TRUCK_TIME_POSTGREE


class MockCursorPsycopg2:
    method_access = ''

    def execute(self, sql) -> None:
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
        sql = f'INSERT INTO public.{FIELD_DISTANCE_TABLE_POSTGREE} ' \
              f'({FIELD_DISTANCE_ID_POSTGREE}, ' \
              f'{FIELD_DISTANCE_ID_ORIGIN_POSTGREE}, ' \
              f'{FIELD_DISTANCE_ID_DESTINATION_POSTGREE}, ' \
              f'{FIELD_DISTANCE_MINUTES_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRAVEL_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_MILES_POSTGREE}, ' \
              f'{FIELD_DISTANCE_KILOMETER_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TIME_AT_POSTGREE}, ' \
              f'{FIELD_DISTANCE_WALK_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRUCK_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRAVEL_TRUCK_TIME_POSTGREE}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'

        with mock.patch.object(DistanceDbService, "db_services") as spy_db_services:
            cursor = MockCursorPsycopg2()
            spy_db_services.conn.cursor.return_value = cursor
            distance_db_service.insert_distances(distance)

        spy_db_services.conn.cursor.assert_called_once()

        spy_db_services.commit.assert_called_once()

        expected_calls_remove_feature = [call(f'{sql}', (
            distance.id_distance,
            distance.id_city_origin,
            distance.id_city_destiny,
            distance.minutes,
            distance.travel_time,
            distance.miles,
            distance.kilometers,
            distance.time_at,
            distance.walk_time,
            distance.truck_time,
            distance.travel_truck_time,
        ))]

        assert spy_db_services.conn.cursor is not None

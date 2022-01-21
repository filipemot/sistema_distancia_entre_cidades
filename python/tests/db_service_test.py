import unittest

from unittest import mock
from unittest.mock import Mock
from mock import patch

import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from services.db_services import DbService


class MockConfigDbService:

    @staticmethod
    def config():
        return {'db_host': 'localhost', 'db_port': '5432', 'db_name': 'test_db'}


class TestDbService(unittest.TestCase):

    @patch("services.db_services.DbService.__init__")
    def test_db_service_connect(self, spy_db_service_init):
        spy_db_service_init.return_value = None

        with mock.patch("psycopg2.connect") as connect:
            connect.return_value = Mock()
            db_service = DbService()
            db_service.config_db_service = MockConfigDbService()
            db_service.connect()
        assert db_service.conn is not None

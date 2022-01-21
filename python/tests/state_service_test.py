import os
import unittest
from typing import List
from unittest import mock
import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from services.state_service import StateService


class StateConfigsService(unittest.TestCase):

    @mock.patch("services.features_service")
    def test_state_configs_service_prepare_data(self, spy_features_service):
        results: List[dict] = [{'Column1': '11', 'Column2': 'RO'}]
        mock_features_service = spy_features_service.return_value
        mock_features_service.excel_to_table.return_value = 'src'
        mock_features_service.find_all.return_value = pd.DataFrame(results)

        state_service = StateService(os.path.dirname(os.path.abspath(__file__)), "config.json")
        state_service.features_service = mock_features_service

        self.assertIs(state_service.features_service, mock_features_service)
        state_service.prepare_data()
        self.assertEqual(state_service.table_state, 'src')
        self.assertEqual(len(state_service.list_values), 1)


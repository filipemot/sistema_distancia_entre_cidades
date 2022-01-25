import unittest

from unittest import mock
from unittest.mock import Mock, patch

import pandas as pd  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore

from models.distance_matrix import DistanceMatrix
from services.base_service import BaseService
from services.distance_service import DistanceService

from utils.constants import DISTANCE_MATRIX_RESULTS_LAYER_NAME, DISTANCE_MATRIX_LAYER_NAME, \
    DISTANCE_MATRIX_TRAVEL_MODE, DISTANCE_MATRIX_TIME_ZONE, DISTANCE_MATRIX_LINE_SHAPE, \
    DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES, DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS, DISTANCE_MATRIX_FIELD_MINUTES, \
    DISTANCE_MATRIX_FIELD_TRAVEL_TIME, DISTANCE_MATRIX_FIELD_MILES, DISTANCE_MATRIX_FIELD_KILOMETERS, \
    DISTANCE_MATRIX_FIELD_TIME_AT, DISTANCE_MATRIX_FIELD_WALK_TIME, DISTANCE_MATRIX_FIELD_TRUCK_TIME, \
    DISTANCE_MATRIX_FIELD_TRUCK_TRAVEL_TIME, DISTANCE_MATRIX_FIELD_NAME


class MockCursorPsycopg2:
    method_access = ''

    def execute(self, sql, parameters=None) -> None:
        print(sql)
        print(parameters)
        self.method_access = self.method_access + 'execute'
        pass

    def close(self) -> None:
        self.method_access = self.method_access + ',close'
        pass


class MockNetworkAnalysisService:
    method_access = ''

    def get_na_class(self, *args):
        self.method_access = 'get_na_class'
        return {'ODLines': 'ODLines'}


class MockFeaturesService:
    method_access = ''

    def get_search_cursor(self, *args):
        self.method_access = 'get_search_cursor'
        return [{'OID': 1, 'SHAPE': 'SHAPE', DISTANCE_MATRIX_FIELD_NAME: '1 - 1'}]

    def read_row(self, *args):
        self.method_access = self.method_access + ',read_row'
        return {DISTANCE_MATRIX_FIELD_NAME: '1 - 1',
                DISTANCE_MATRIX_FIELD_MINUTES: DISTANCE_MATRIX_FIELD_MINUTES,
                DISTANCE_MATRIX_FIELD_TRAVEL_TIME: DISTANCE_MATRIX_FIELD_TRAVEL_TIME,
                DISTANCE_MATRIX_FIELD_MILES: DISTANCE_MATRIX_FIELD_MILES,
                DISTANCE_MATRIX_FIELD_KILOMETERS: DISTANCE_MATRIX_FIELD_KILOMETERS,
                DISTANCE_MATRIX_FIELD_TIME_AT: DISTANCE_MATRIX_FIELD_TIME_AT,
                DISTANCE_MATRIX_FIELD_WALK_TIME: DISTANCE_MATRIX_FIELD_WALK_TIME,
                DISTANCE_MATRIX_FIELD_TRUCK_TIME: DISTANCE_MATRIX_FIELD_TRUCK_TIME,
                DISTANCE_MATRIX_FIELD_TRUCK_TRAVEL_TIME: DISTANCE_MATRIX_FIELD_TRUCK_TRAVEL_TIME}


class MockMatrixLayer:
    method_access = ''
    matrix_sub_layer = None

    def getOutput(self, *args, **kwargs):
        self.matrix_sub_layer = MockMatrixSubLayer()
        self.method_access = 'getOutput'
        return self.matrix_sub_layer


class MockMatrixSubLayer:
    method_access = ''

    def listLayers(self, *args, **kwargs):
        self.method_access = 'listLayers'
        return 'layers'


class TestDistanceService(unittest.TestCase):

    @patch("services.distance_service.DistanceService.__init__")
    def test_distance_service_prepare_data(self, spy_distance_service_init):
        spy_distance_service_init.return_value = None

        distance_service = DistanceService('', '', Mock())

        distance_service.distance_db_services = Mock()
        distance_service.network_analysis_service = Mock()
        distance_service.prepare_data()
        distance_service.network_analysis_service.remove_dataset_matrix.assert_called_once()
        distance_service.distance_db_services.delete_all_distances.assert_called_once()

    @patch("services.distance_service.DistanceService.__init__")
    def test_distance_service_calculate_distances(self, spy_distance_service_init):
        spy_distance_service_init.return_value = None

        distance_service = DistanceService('', '', Mock())

        distance_service.distance_db_services = Mock()
        distance_service.network_analysis_service = Mock()
        distance_service.feature_service = Mock()
        distance_service.distance_calculate_layer = DISTANCE_MATRIX_RESULTS_LAYER_NAME

        with mock.patch.object(BaseService, "configs", {'route': 'ROUTE', 'execution': {'clear_distance': 1}}):
            distance_service.distance_matrix = DistanceMatrix(distance_service.configs['route'],
                                                              DISTANCE_MATRIX_LAYER_NAME,
                                                              DISTANCE_MATRIX_TRAVEL_MODE,
                                                              DISTANCE_MATRIX_TIME_ZONE,
                                                              DISTANCE_MATRIX_LINE_SHAPE,
                                                              DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES,
                                                              DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS)
            with mock.patch.object(DistanceService, "prepare_data") as spy_prepare_data:
                with mock.patch.object(DistanceService, "_DistanceService__location_origin") \
                        as spy_location_origin:
                    with mock.patch.object(DistanceService, "_DistanceService__location_destination") \
                            as spy_location_destination:
                        with mock.patch.object(DistanceService, "get_layer_matrix_distance") \
                                as spy_get_layer_matrix_distance:
                            spy_get_layer_matrix_distance.return_value = 'Lines'
                            spy_location_origin.return_value = None
                            spy_location_destination.return_value = None
                            spy_prepare_data.return_value = None
                            distance_service.layer_cost = \
                                distance_service.network_analysis_service.create_dataset_cost_matrix.return_value = \
                                'layer_cost'
                            distance_service.calculate_distances()
                            distance_service.network_analysis_service.solve_matrix_distance.return_value = None
                            distance_service.network_analysis_service.solve_matrix_distance.assert_called_once()
                            distance_service.feature_service.copy_features.return_value = None
                            distance_service.feature_service.copy_features.assert_called_once()
                            distance_service.network_analysis_service.remove_dataset_matrix.return_value = None
                            distance_service.network_analysis_service.remove_dataset_matrix.assert_called_once()

    @patch("services.distance_service.DistanceService.__init__")
    def test_distance_service_save_distance(self, spy_distance_service_init):
        spy_distance_service_init.return_value = None

        distance_service = DistanceService('', '', Mock())

        mock_feature_service = MockFeaturesService()

        distance_service.distance_db_services = Mock()
        distance_service.network_analysis_service = Mock()
        distance_service.feature_service = mock_feature_service
        distance_service.distance_calculate_layer = DISTANCE_MATRIX_RESULTS_LAYER_NAME

        with mock.patch.object(BaseService, "configs", {'route': 'ROUTE', 'execution': {'save_distance': 1}}):
            distance_service.distance_db_services.delete_all_distances.return_value = None
            distance_service.distance_db_services.insert_distances.return_value = None

            distance_service.save_distance()
            distance_service.distance_db_services.delete_all_distances.assert_called_once()
            distance_service.distance_db_services.insert_distances.assert_called_once()
            assert mock_feature_service.method_access == 'get_search_cursor,read_row'

    @patch("services.distance_service.DistanceService.__init__")
    def test_distance_service_remove_feature(self, spy_distance_service_init):
        spy_distance_service_init.return_value = None

        distance_service = DistanceService('', '', Mock())

        distance_service.feature_service = Mock()
        distance_service.network_analysis_service = Mock()
        distance_service.city_services = Mock()
        distance_service.distance_calculate_layer = DISTANCE_MATRIX_RESULTS_LAYER_NAME

        distance_service.remove_feature()
        distance_service.feature_service.remove_feature.assert_called_once()
        distance_service.network_analysis_service.remove_dataset_matrix.assert_called_once()
        distance_service.city_services.remove_feature.assert_called_once()

    @patch("services.distance_service.DistanceService.__init__")
    def test_distance_service_get_layer_matrix_distance(self, spy_distance_service_init):
        spy_distance_service_init.return_value = None

        distance_service = DistanceService('', '', Mock())

        network_analysis_service = MockNetworkAnalysisService()
        matrix_layer = MockMatrixLayer()

        distance_service.city_services = Mock()
        distance_service.distance_calculate_layer = DISTANCE_MATRIX_RESULTS_LAYER_NAME
        distance_service.network_analysis_service = network_analysis_service

        distance_service.get_layer_matrix_distance(matrix_layer)
        assert network_analysis_service.method_access == 'get_na_class'
        assert matrix_layer.method_access == 'getOutput'
        assert matrix_layer.matrix_sub_layer is not None
        assert matrix_layer.matrix_sub_layer.method_access == 'listLayers'

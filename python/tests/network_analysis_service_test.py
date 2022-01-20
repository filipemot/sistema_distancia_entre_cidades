import os
import unittest

import arcpy  # type: ignore

from arcgisscripting import ExecuteError  # type: ignore
from arcpy import env

from models.distance_matrix import DistanceMatrix
from services.configs_service import ConfigsService
from services.network_analysis_service import NetworkAnalysisService
from utils.constants import DISTANCE_MATRIX_LAYER_NAME, DISTANCE_MATRIX_TRAVEL_MODE, DISTANCE_MATRIX_TIME_ZONE, \
    DISTANCE_MATRIX_LINE_SHAPE, DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES, DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS, \
    NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS


class TestNetworkAnalysisService(unittest.TestCase):
    TEST_GDB = 'in_memory'
    network_analysis_service: NetworkAnalysisService = NetworkAnalysisService()

    def setUp(self) -> None:
        self.configs_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.configs = self.configs_service.data_config
        env.workspace = self.TEST_GDB
        self.distance_matrix: DistanceMatrix = DistanceMatrix(self.configs['route'],
                                                              DISTANCE_MATRIX_LAYER_NAME,
                                                              DISTANCE_MATRIX_TRAVEL_MODE,
                                                              DISTANCE_MATRIX_TIME_ZONE,
                                                              DISTANCE_MATRIX_LINE_SHAPE,
                                                              DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES,
                                                              DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS)

    def test_create_dataset_cost_matrix(self):
        layer_cost = self.network_analysis_service.create_dataset_cost_matrix(self.distance_matrix)
        exists = arcpy.Exists(layer_cost)
        assert exists is True

    def test_remove_dataset_matrix(self):
        self.network_analysis_service.create_dataset_cost_matrix(self.distance_matrix)
        self.network_analysis_service.remove_dataset_matrix()
        datasets = arcpy.ListDatasets(NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS)
        qtd_datasets_after_remove = len(datasets)

        assert qtd_datasets_after_remove == 0

    def tearDown(self):
        arcpy.Delete_management(self.TEST_GDB)

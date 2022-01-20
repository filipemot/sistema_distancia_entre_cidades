import os
import unittest

import arcpy  # type: ignore
from arcgisscripting import ExecuteError  # type: ignore
from arcpy import env

from models.distance_matrix import DistanceMatrix
from models.location import Location

from services.configs_service import ConfigsService
from services.features_service import FeaturesService
from services.network_analysis_service import NetworkAnalysisService

from utils.constants import DISTANCE_MATRIX_LAYER_NAME, DISTANCE_MATRIX_TRAVEL_MODE, DISTANCE_MATRIX_TIME_ZONE, \
    DISTANCE_MATRIX_LINE_SHAPE, DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES, DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS, \
    NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS, NETWORK_ANALYTICS_ORIGIN_TYPE, \
    NETWORK_ANALYTICS_ORIGIN_FIELD_MAPPING, NETWORK_ANALYTICS_ORIGIN_SEARCH_CRITERIA, \
    NETWORK_ANALYTICS_ORIGIN_SEARCH_TOLERANCE, NETWORK_ANALYTICS_ORIGIN_FIND_CLOSEST, \
    NETWORK_ANALYTICS_ORIGIN_APPEND_LOCATION, NETWORK_ANALYTICS_ORIGIN_SNAP, NETWORK_ANALYTICS_ORIGIN_SNAP_OFFSET, \
    NETWORK_ANALYTICS_ORIGIN_EXCLUDE_RESTRICTED, NETWORK_ANALYTICS_DESTINATION_TYPE, \
    NETWORK_ANALYTICS_DESTINATION_FIELD_MAPPING, NETWORK_ANALYTICS_DESTINATION_SEARCH_CRITERIA, \
    NETWORK_ANALYTICS_DESTINATION_SEARCH_TOLERANCE, NETWORK_ANALYTICS_DESTINATION_FIND_CLOSEST, \
    NETWORK_ANALYTICS_DESTINATION_APPEND_LOCATION, NETWORK_ANALYTICS_DESTINATION_SNAP, \
    NETWORK_ANALYTICS_DESTINATION_SNAP_OFFSET, NETWORK_ANALYTICS_DESTINATION_EXCLUDE_RESTRICTED, \
    NETWORK_ANALYTICS_IGNORE_INVALID_LOCATIONS, NETWORK_ANALYTICS_TERMINATE_ON_ERROR, FIELD_STATE, TYPE_TEXT, \
    FIELD_CITY_OBJECT_ID, FIELD_CITY_ID, FIELD_CITY_LAT, TYPE_FLOAT, FIELD_CITY_LNG_STR, TYPE_DOUBLE, FIELD_CITY_LNG, \
    FIELD_CITY_LAT_STR, FEATURE_CITY, SHEET_NAME_CITY, FEATURE_CITY_POINT


class TestNetworkAnalysisService(unittest.TestCase):
    TEST_GDB = 'in_memory'
    network_analysis_service: NetworkAnalysisService = NetworkAnalysisService()

    def setUp(self) -> None:
        self.configs_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.configs = self.configs_service.data_config
        self.features_service = FeaturesService()
        self.table_city: str = ''
        self.TEST_GDB = self.configs['workspace']
        self.table_city_geo = self.configs['workspace'] + "\\" + FEATURE_CITY_POINT

        self.__create_table()
        self.__add_fields_in_table()
        self.features_service.convert_table_to_point(self.table_city, self.table_city_geo,
                                                     FIELD_CITY_LAT, FIELD_CITY_LNG)

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
        layer_cost = self.network_analysis_service.create_dataset_cost_matrix(self.distance_matrix)
        self.__location_origin(layer_cost)
        self.__location_destination(layer_cost)
        self.network_analysis_service.solve_matrix_distance(layer_cost,
                                                            NETWORK_ANALYTICS_IGNORE_INVALID_LOCATIONS,
                                                            NETWORK_ANALYTICS_TERMINATE_ON_ERROR)

        datasets = arcpy.ListDatasets(NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS)
        qtd_datasets_after_remove = len(datasets)

        self.network_analysis_service.remove_dataset_matrix()
        datasets = arcpy.ListDatasets(NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS)
        qtd_datasets_before_remove = len(datasets)

        assert qtd_datasets_before_remove == 0 and qtd_datasets_after_remove == 1

    def __location_origin(self, layer_cost) -> None:
        location_origin: Location = Location(layer_cost,
                                             NETWORK_ANALYTICS_ORIGIN_TYPE,
                                             self.table_city_geo,
                                             NETWORK_ANALYTICS_ORIGIN_FIELD_MAPPING,
                                             NETWORK_ANALYTICS_ORIGIN_SEARCH_CRITERIA,
                                             NETWORK_ANALYTICS_ORIGIN_SEARCH_TOLERANCE,
                                             NETWORK_ANALYTICS_ORIGIN_FIND_CLOSEST,
                                             NETWORK_ANALYTICS_ORIGIN_APPEND_LOCATION,
                                             NETWORK_ANALYTICS_ORIGIN_SNAP,
                                             NETWORK_ANALYTICS_ORIGIN_SNAP_OFFSET,
                                             NETWORK_ANALYTICS_ORIGIN_EXCLUDE_RESTRICTED)
        self.network_analysis_service.add_locations(location_origin)

    def __location_destination(self, layer_cost) -> None:
        location_destination: Location = Location(layer_cost,
                                                  NETWORK_ANALYTICS_DESTINATION_TYPE,
                                                  self.table_city_geo,
                                                  NETWORK_ANALYTICS_DESTINATION_FIELD_MAPPING,
                                                  NETWORK_ANALYTICS_DESTINATION_SEARCH_CRITERIA,
                                                  NETWORK_ANALYTICS_DESTINATION_SEARCH_TOLERANCE,
                                                  NETWORK_ANALYTICS_DESTINATION_FIND_CLOSEST,
                                                  NETWORK_ANALYTICS_DESTINATION_APPEND_LOCATION,
                                                  NETWORK_ANALYTICS_DESTINATION_SNAP,
                                                  NETWORK_ANALYTICS_DESTINATION_SNAP_OFFSET,
                                                  NETWORK_ANALYTICS_DESTINATION_EXCLUDE_RESTRICTED)
        self.network_analysis_service.add_locations(location_destination)

    def __create_table(self) -> None:
        self.table_city = self.features_service.excel_to_table(
            self.configs['excel_city'],
            self.configs['workspace'],
            FEATURE_CITY,
            SHEET_NAME_CITY)

    def __add_fields_in_table(self) -> None:
        self.features_service.add_field_in_table(self.table_city, FIELD_STATE, TYPE_TEXT)
        self.features_service.add_computed_field(self.table_city, FIELD_CITY_ID, f'!{FIELD_CITY_OBJECT_ID}!', TYPE_TEXT)
        self.features_service.add_computed_field(self.table_city, f'{FIELD_CITY_LAT}',
                                                 f'{TYPE_FLOAT}(!{FIELD_CITY_LNG_STR}!)', TYPE_DOUBLE)
        self.features_service.add_computed_field(self.table_city, f'{FIELD_CITY_LNG}',
                                                 f'{TYPE_FLOAT}(!{FIELD_CITY_LAT_STR}!)', TYPE_DOUBLE)

    def tearDown(self):
        arcpy.Delete_management(self.TEST_GDB + '/' + FEATURE_CITY)
        arcpy.Delete_management(self.table_city_geo)
        self.network_analysis_service.remove_dataset_matrix()


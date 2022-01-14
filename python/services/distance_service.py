import time

from arcpy import env  # type: ignore

from models.distance_matrix import DistanceMatrix
from models.location import Location
from services.base_service import BaseService
from services.city_service import CityService
from services.distance_db_service import DistanceDbService
from services.features_service import FeaturesService
from services.network_analysis_service import NetworkAnalysisService
from utils.constants import DISTANCE_MATRIX_LAYER_NAME, DISTANCE_MATRIX_TRAVEL_MODE, DISTANCE_MATRIX_TIME_ZONE, \
    DISTANCE_MATRIX_LINE_SHAPE, DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES, DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS, \
    NETWORK_ANALYTICS_ORIGIN_TYPE, NETWORK_ANALYTICS_ORIGIN_FIELD_MAPPING, \
    NETWORK_ANALYTICS_ORIGIN_SEARCH_CRITERIA, NETWORK_ANALYTICS_ORIGIN_FIND_CLOSEST, \
    NETWORK_ANALYTICS_ORIGIN_APPEND_LOCATION, NETWORK_ANALYTICS_ORIGIN_SNAP, NETWORK_ANALYTICS_ORIGIN_SNAP_OFFSET, \
    NETWORK_ANALYTICS_ORIGIN_EXCLUDE_RESTRICTED, NETWORK_ANALYTICS_ORIGIN_SEARCH_TOLERANCE, \
    NETWORK_ANALYTICS_DESTINATION_TYPE, NETWORK_ANALYTICS_DESTINATION_FIELD_MAPPING, \
    NETWORK_ANALYTICS_DESTINATION_SEARCH_TOLERANCE, NETWORK_ANALYTICS_DESTINATION_SEARCH_CRITERIA, \
    NETWORK_ANALYTICS_DESTINATION_FIND_CLOSEST, NETWORK_ANALYTICS_DESTINATION_APPEND_LOCATION, \
    NETWORK_ANALYTICS_DESTINATION_SNAP, NETWORK_ANALYTICS_DESTINATION_SNAP_OFFSET, \
    NETWORK_ANALYTICS_DESTINATION_EXCLUDE_RESTRICTED, NETWORK_ANALYTICS_IGNORE_INVALID_LOCATIONS, \
    NETWORK_ANALYTICS_TERMINATE_ON_ERROR, DISTANCE_MATRIX_RESULTS_LAYER_NAME
from utils.timer_decorator import timer_decorator


class DistanceService(BaseService):

    def __init__(self, folder_path: str, file_name: str, city_services: CityService) -> None:
        super().__init__(folder_path, file_name)
        env.workspace = self.configs["workspace"]
        self.distance_db_services: DistanceDbService = DistanceDbService()
        self.city_services: CityService = city_services
        self.network_analysis_service: NetworkAnalysisService = NetworkAnalysisService()
        self.layer_cost: str = ''
        self.distance_matrix: DistanceMatrix = DistanceMatrix(self.configs['route'],
                                                              DISTANCE_MATRIX_LAYER_NAME,
                                                              DISTANCE_MATRIX_TRAVEL_MODE,
                                                              DISTANCE_MATRIX_TIME_ZONE,
                                                              DISTANCE_MATRIX_LINE_SHAPE,
                                                              DISTANCE_MATRIX_ACCUMULATE_ATTRIBUTES,
                                                              DISTANCE_MATRIX_IGNORE_INVALID_LOCATIONS)
        self.feature_service = FeaturesService()
        self.distance_calculate_layer = self.configs['workspace'] + "\\" + DISTANCE_MATRIX_RESULTS_LAYER_NAME

    @timer_decorator('DistanceService.prepare_data')
    def prepare_data(self) -> None:
        self.distance_db_services.delete_all_distances()
        self.network_analysis_service.remove_dataset_matrix()

    def calculate_distances(self) -> None:
        if self.configs['execution']['clear_distance'] == 1:
            self.prepare_data()
            self.layer_cost = self.network_analysis_service.create_dataset_cost_matrix(self.distance_matrix)
            self.__location_origin()
            self.__location_destination()
            self.network_analysis_service.solve_matrix_distance(self.layer_cost,
                                                                NETWORK_ANALYTICS_IGNORE_INVALID_LOCATIONS,
                                                                NETWORK_ANALYTICS_TERMINATE_ON_ERROR)
            self.feature_service.copy_features(self.get_layer_matrix_distance(self.layer_cost),
                                               self.distance_calculate_layer)
            self.network_analysis_service.remove_dataset_matrix()

    def get_layer_matrix_distance(self, object_matrix_layer):
        na_class = self.network_analysis_service.get_na_class(object_matrix_layer)
        layer_object = object_matrix_layer.getOutput(0)
        lines_sublayer = layer_object.listLayers(na_class["ODLines"])[0]
        return lines_sublayer


    def __location_origin(self) -> None:
        location_origin: Location = Location(self.layer_cost,
                                             NETWORK_ANALYTICS_ORIGIN_TYPE,
                                             self.city_services.table_city_geo,
                                             NETWORK_ANALYTICS_ORIGIN_FIELD_MAPPING,
                                             NETWORK_ANALYTICS_ORIGIN_SEARCH_CRITERIA,
                                             NETWORK_ANALYTICS_ORIGIN_SEARCH_TOLERANCE,
                                             NETWORK_ANALYTICS_ORIGIN_FIND_CLOSEST,
                                             NETWORK_ANALYTICS_ORIGIN_APPEND_LOCATION,
                                             NETWORK_ANALYTICS_ORIGIN_SNAP,
                                             NETWORK_ANALYTICS_ORIGIN_SNAP_OFFSET,
                                             NETWORK_ANALYTICS_ORIGIN_EXCLUDE_RESTRICTED)
        self.network_analysis_service.add_locations(location_origin)

    def __location_destination(self) -> None:
        location_destination: Location = Location(self.layer_cost,
                                                  NETWORK_ANALYTICS_DESTINATION_TYPE,
                                                  self.city_services.table_city_geo,
                                                  NETWORK_ANALYTICS_DESTINATION_FIELD_MAPPING,
                                                  NETWORK_ANALYTICS_DESTINATION_SEARCH_CRITERIA,
                                                  NETWORK_ANALYTICS_DESTINATION_SEARCH_TOLERANCE,
                                                  NETWORK_ANALYTICS_DESTINATION_FIND_CLOSEST,
                                                  NETWORK_ANALYTICS_DESTINATION_APPEND_LOCATION,
                                                  NETWORK_ANALYTICS_DESTINATION_SNAP,
                                                  NETWORK_ANALYTICS_DESTINATION_SNAP_OFFSET,
                                                  NETWORK_ANALYTICS_DESTINATION_EXCLUDE_RESTRICTED)
        self.network_analysis_service.add_locations(location_destination)

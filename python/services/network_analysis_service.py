import logging
import time

import arcpy  # type: ignore

from models.distance_matrix import DistanceMatrix
from models.location import Location
from utils.constants import NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS, NETWORK_ANALYTICS_LICENCE, \
    LICENCE_AVAILABLE
from utils.timer_decorator import timer_decorator


class NetworkAnalysisService:

    def __init__(self):
        self.__check_extension_network()

    @staticmethod
    @timer_decorator('NetworkAnalysisService.prepare_data')
    def create_dataset_cost_matrix(distance_matrix: DistanceMatrix):
        cost_matrix_result = arcpy.na.MakeODCostMatrixAnalysisLayer(distance_matrix.layer_route,
                                                                    distance_matrix.layer_cost_name,
                                                                    distance_matrix.travel_mode,
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    distance_matrix.time_zone,
                                                                    distance_matrix.line_shape,
                                                                    distance_matrix.accumulate_attributes,
                                                                    distance_matrix.ignore_invalid_locations)

        return cost_matrix_result

    @staticmethod
    @timer_decorator('NetworkAnalysisService.remove_dataset_matrix')
    def remove_dataset_matrix():
        datasets = arcpy.ListDatasets(NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS)

        for dataset in datasets:
            arcpy.Delete_management(dataset)

    @staticmethod
    @timer_decorator('NetworkAnalysisService.add_locations')
    def add_locations(location: Location):
        arcpy.na.AddLocations(location.layer_matrix_name,
                              location.type_locations,
                              location.source_layer,
                              location.field_mapping,
                              location.search_tolerance,
                              None,
                              location.search_criteria,
                              location.find_closest,
                              location.append_location,
                              location.snap,
                              location.snap_offset,
                              location.exclude_restricted,
                              None)

    @staticmethod
    @timer_decorator('NetworkAnalysisService.solve_matrix_distance')
    def solve_matrix_distance(layer_matrix_name, ignore_invalid_locations, terminate_on_error):
        arcpy.na.Solve(layer_matrix_name,
                       ignore_invalid_locations,
                       terminate_on_error,
                       None,
                       '')
        ends = time.time()

    @staticmethod
    def __get_na_class(object_matrix_layer):
        layer_object = object_matrix_layer.getOutput(0)

        return arcpy.na.GetNAClassNames(layer_object)

    @staticmethod
    def get_na_class(object_matrix_layer):
        layer_object = object_matrix_layer.getOutput(0)

        return arcpy.na.GetNAClassNames(layer_object)

    @staticmethod
    def __check_extension_network():
        if arcpy.CheckExtension(NETWORK_ANALYTICS_LICENCE) == LICENCE_AVAILABLE:
            arcpy.CheckOutExtension(NETWORK_ANALYTICS_LICENCE)
        else:
            logging.error("Network Analyst extension is not available.")
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

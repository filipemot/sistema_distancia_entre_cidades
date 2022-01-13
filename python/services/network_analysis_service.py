import logging
import time

import arcpy  # type: ignore

from models.distance_matrix import DistanceMatrix
from models.location import Location
from utils.constants import NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS, NETWORK_ANALYTICS_LICENCE, \
    LICENCE_AVAILABLE


class NetworkAnalysisService:

    def __init__(self):
        self.__check_extension_network()

    @staticmethod
    def create_dataset_cost_matrix(distance_matrix: DistanceMatrix):
        initial = time.time()
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

        ends = time.time()
        print("create_dataset_cost_matrix:" + ends - initial)
        return cost_matrix_result

    @staticmethod
    def remove_dataset_matrix():
        datasets = arcpy.ListDatasets(NETWORK_ANALYTICS_DATASET_NAME, TYPE_LIST_DATASETS)

        for dataset in datasets:
            arcpy.Delete_management(dataset)

    @staticmethod
    def add_locations(location: Location):
        initial = time.time()
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
        ends = time.time()
        print("add_locations:" + ends - initial)

    @staticmethod
    def solve_matrix_distance(layer_matrix_name, ignore_invalid_locations, terminate_on_error):
        initial = time.time()
        arcpy.na.Solve(layer_matrix_name,
                       ignore_invalid_locations,
                       terminate_on_error,
                       None,
                       '')
        ends = time.time()
        print("solve_matrix_distance:" + ends - initial)

    @staticmethod
    def __get_na_class(object_matrix_layer):
        layer_object = object_matrix_layer.getOutput(0)

        return arcpy.na.GetNAClassNames(layer_object)


    @staticmethod
    def __check_extension_network():
        if arcpy.CheckExtension(NETWORK_ANALYTICS_LICENCE) == LICENCE_AVAILABLE:
            arcpy.CheckOutExtension(NETWORK_ANALYTICS_LICENCE)
        else:
            logging.error("Network Analyst extension is not available.")
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

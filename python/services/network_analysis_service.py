import arcpy


class NetworkAnalysisService:

    def __init__(self):
        self.check_extension_network()

    @staticmethod
    def create_dataset_cost_matrix(layer_route, layer_cost_name):
        cost_matrix_result = arcpy.na.MakeODCostMatrixAnalysisLayer(layer_route, layer_cost_name, "Driving Time", None,
                                                                    None,
                                                                    None, "LOCAL_TIME_AT_LOCATIONS", "STRAIGHT_LINES",
                                                                    "Kilometers;Minutes;TravelTime", "SKIP")

        return cost_matrix_result

    @staticmethod
    def remove_dataset_matrix():
        datasets = arcpy.ListDatasets("ODCostMatrixSolver*", "ALL")

        for dataset in datasets:
            arcpy.Delete_management(dataset)

    @staticmethod
    def check_extension_network():
        if arcpy.CheckExtension("network") == "Available":
            arcpy.CheckOutExtension("network")
        else:
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

    @staticmethod
    def add_locations(layer_matrix_name, type_locations, source_layer, id_field):
        arcpy.na.AddLocations(layer_matrix_name, type_locations, source_layer, f"Name {id_field} #;CurbApproach # 0",
                              "5000 Meters", None,
                              "Routing_Streets SHAPE;Routing_Streets_Override NONE;Routing_ND_Junctions NONE",
                              "MATCH_TO_CLOSEST", "CLEAR", "NO_SNAP", "5 Meters", "EXCLUDE", None)

    @staticmethod
    def solve_matrix_distance(layer_matrix_name):
        arcpy.na.Solve(layer_matrix_name, "SKIP", "TERMINATE", "1 Kilometers", '')

    @staticmethod
    def get_na_class(object_matrix_layer):
        layer_object = object_matrix_layer.getOutput(0)

        return arcpy.na.GetNAClassNames(layer_object)
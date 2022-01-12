class DistanceMatrix:

    def __init__(self, layer_route: str, layer_cost_name: str, travel_mode: str, time_zone: str, line_shape: str,
                 accumulate_attributes: str, ignore_invalid_locations: str):
        self.layer_route: str = layer_route
        self.layer_cost_name: str = layer_cost_name
        self.travel_mode: str = travel_mode
        self.time_zone: str = time_zone
        self.line_shape: str = line_shape
        self.accumulate_attributes: str = accumulate_attributes
        self.ignore_invalid_locations: str = ignore_invalid_locations
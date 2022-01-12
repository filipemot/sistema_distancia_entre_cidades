class Location:
    def __init__(self, layer_matrix_name: str, type_locations: str, source_layer: str, field_mapping: str,
                 search_criteria: str, search_tolerance: str, find_closest: str, append_location: str, snap: str,
                 snap_offset: str, exclude_restricted: str):
        self.layer_matrix_name: str = layer_matrix_name
        self.type_locations: str = type_locations
        self.source_layer: str = source_layer
        self.field_mapping: str = field_mapping
        self.search_criteria: str = search_criteria
        self.search_tolerance: str = search_tolerance
        self.find_closest: str = find_closest
        self.append_location: str = append_location
        self.snap: str = snap
        self.snap_offset: str = snap_offset
        self.exclude_restricted: str = exclude_restricted

import uuid  # type: ignore


class Distance:

    def __init__(self, id_city_origin: int, id_city_destiny: int, minutes: float,
                 travel_time: float, miles: float, kilometers: float, time_at: float, walk_time: float,
                 truck_time: float, travel_truck_time: float) -> None:
        self.id_distance: uuid = str(uuid.uuid4())  # type: ignore
        self.id_city_origin: int = id_city_origin
        self.id_city_destiny: int = id_city_destiny
        self.minutes: float = minutes
        self.travel_time: float = travel_time
        self.miles: float = miles
        self.kilometers: float = kilometers
        self.time_at: float = time_at
        self.walk_time: float = walk_time
        self.truck_time: float = truck_time
        self.travel_truck_time: float = travel_truck_time

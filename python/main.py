import os

from services.city_service import CityService
from services.distance_service import DistanceService
from services.state_service import StateService


def main():
    state_services: StateService = StateService(os.path.dirname(os.path.abspath(__file__)), "config.json")

    city_services: CityService = CityService(os.path.dirname(os.path.abspath(__file__)), "config.json",
                                             state_services)

    distance_services: DistanceService = DistanceService(os.path.dirname(os.path.abspath(__file__)), "config.json",
                                                         city_services)
    distance_services.calculate_distances()


if __name__ == '__main__':
    main()

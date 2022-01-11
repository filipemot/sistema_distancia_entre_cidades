import os

from services.city_services import CityServices
from services.state_services import StateServices


def main():
    state_services = StateServices(os.path.dirname(os.path.abspath(__file__)), "config.json")

    city_services = CityServices(os.path.dirname(os.path.abspath(__file__)), "config.json", state_services)


if __name__ == '__main__':
    main()

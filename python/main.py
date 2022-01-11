import os

from services.city_services import CityServices
from services.state_services import StateServices


def main():
    state = StateServices(os.path.dirname(os.path.abspath(__file__)), "config.json")

    city = CityServices(os.path.dirname(os.path.abspath(__file__)), "config.json", state)


if __name__ == '__main__':
    main()

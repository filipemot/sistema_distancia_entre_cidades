import os

from models.city import City
from models.state import State


def main():
    city = City(os.path.dirname(os.path.abspath(__file__)), "config.json")
    state = State(os.path.dirname(os.path.abspath(__file__)), "config.json")


if __name__ == '__main__':
    main()

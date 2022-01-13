from services.base_service import BaseService
from services.city_service import CityService
from services.distance_db_service import DistanceDbService


class DistanceService(BaseService):

    def __init__(self, folder_path: str, file_name: str, city_services: CityService) -> None:
        super().__init__(folder_path, file_name)
        self.distance_db_services: DistanceDbService = DistanceDbService()
        self.city_services: CityService = city_services

    def prepare_data(self) -> None:
        self.distance_db_services.delete_all_distances()


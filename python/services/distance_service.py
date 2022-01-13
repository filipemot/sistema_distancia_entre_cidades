from services.base_service import BaseService
from services.city_service import CityService
from services.distance_db_service import DistanceDbService
from services.network_analysis_service import NetworkAnalysisService


class DistanceService(BaseService):

    def __init__(self, folder_path: str, file_name: str, city_services: CityService) -> None:
        super().__init__(folder_path, file_name)
        self.distance_db_services: DistanceDbService = DistanceDbService()
        self.city_services: CityService = city_services
        self.network_analysis_service: NetworkAnalysisService = NetworkAnalysisService()

    def prepare_data(self) -> None:
        self.distance_db_services.delete_all_distances()
        self.network_analysis_service.remove_dataset_matrix()


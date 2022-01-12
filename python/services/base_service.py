import abc

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


class BaseService(metaclass=abc.ABCMeta):

    def __init__(self, folder_path: str, file_name: str) -> None:
        self.config_service: ConfigsService = ConfigsService(folder_path, file_name)
        self.features_service: FeaturesService = FeaturesService()

    @property
    def configs(self):
        return self.config_service.data_config

    @abc.abstractmethod
    def create_table(self) -> None:
        ...

    @abc.abstractmethod
    def prepare_data(self) -> None:
        ...

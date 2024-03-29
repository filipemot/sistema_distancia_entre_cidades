import abc

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


class BaseService(metaclass=abc.ABCMeta):
    features_service: FeaturesService
    config_service: ConfigsService

    def __init__(self, folder_path: str, file_name: str) -> None:
        self.config_service = ConfigsService(folder_path, file_name)
        self.features_service = FeaturesService()

    @property
    def configs(self):
        return self.config_service.data_config

    @abc.abstractmethod
    def prepare_data(self) -> None:
        ...

    @abc.abstractmethod
    def remove_feature(self) -> None:
        ...
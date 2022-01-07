import abc

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


class ModelsBase(metaclass=abc.ABCMeta):

    def __init__(self, folder_path, file_name):
        self.config_service = ConfigsService(folder_path, file_name)
        self.features_service = FeaturesService()

    @property
    def configs(self):
        return self.config_service.data_config

    @abc.abstractmethod
    def create_table(self):
        ...

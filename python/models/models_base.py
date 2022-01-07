import abc

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


class ModelsBase(metaclass=abc.ABCMeta):

    def __init__(self, folder_path, file_name):
        config_service = ConfigsService(folder_path, file_name)
        self.configs = config_service.data_config
        self.features_service = FeaturesService()

    @abc.abstractmethod
    def create_table(self):
        ...

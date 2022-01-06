import os

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


def read_configs():
    config_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config.json")
    return config_service.data_config


def main():
    features_service = FeaturesService()

    configs = read_configs()
    table_city = features_service.excel_to_table(configs['excel_city'], configs['workspace'], "city", "municipios")
    table_states = features_service.excel_to_table(configs['excel_states'], configs['workspace'], "state", "estados")

if __name__ == '__main__':
    main()

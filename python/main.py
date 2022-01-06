import os

from services.configs_service import ConfigsService
from services.features_service import FeaturesService


def main():
    config_service = ConfigsService(os.path.dirname(os.path.abspath(__file__)), "config.json")
    features_service = FeaturesService()

    configs = config_service.data_config

    table_city = features_service.excel_to_table(configs['excel_city'], configs['workspace'], "city", "municipios")
    table_states = features_service.excel_to_table(configs['excel_states'], configs['workspace'], "state", "estados")


if __name__ == '__main__':
    main()

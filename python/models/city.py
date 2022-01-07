from models.models_base import ModelsBase
from utils.constants import FEATURE_CITY, SHEET_NAME_CITY, FIELD_STATE, FIELD_CITY_ID


class City(ModelsBase):

    def __init__(self, folder_path, file_name, state):
        super().__init__(folder_path, file_name)
        self.state = state
        self.table_city = None
        self.prepare_data()

    def prepare_data(self):
        self.create_table()
        self.features_service.add_field_in_table(self.table_city, FIELD_STATE, 'Text')
        self.features_service.add_computed_field(self.table_city, FIELD_CITY_ID, '!OBJECTID!')

    def create_table(self):
        self.table_city = self.features_service.excel_to_table(
            self.configs['excel_city'], 
            self.configs['workspace'], 
            FEATURE_CITY,
            SHEET_NAME_CITY)

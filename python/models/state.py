from models.models_base import ModelsBase
from utils.constants import FEATURE_STATE, SHEET_NAME_STATE


class State(ModelsBase):

    def __init__(self, folder_path, file_name):
        super().__init__(folder_path, file_name)
        self.table_city = None
        self.create_table()

    def create_table(self):
        self.table_city = self.features_service.excel_to_table(
            self.configs['excel_states'],
            self.configs['workspace'], 
            FEATURE_STATE,
            SHEET_NAME_STATE)

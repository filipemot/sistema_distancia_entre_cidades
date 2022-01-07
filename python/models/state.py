from models.models_base import ModelsBase
from utils.constants import FEATURE_STATE, SHEET_NAME_STATE


class State(ModelsBase):

    def __init__(self, folder_path, file_name):
        super().__init__(folder_path, file_name)
        self._table_state = None
        self.create_table()

    @property
    def table_state(self):
        return self._table_state

    @table_state.setter
    def table_state(self, table_state_value):
        self._table_state = table_state_value

    def create_table(self):
        self._table_state = self.features_service.excel_to_table(
            self.configs['excel_states'],
            self.configs['workspace'],
            FEATURE_STATE,
            SHEET_NAME_STATE)

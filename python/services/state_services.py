from typing import List

import pandas as pd  # type: ignore

from services.base_services import BaseServices
from utils.constants import FEATURE_STATE, SHEET_NAME_STATE, STATE_FIELD_UF, STATE_FIELD_ID


class StateServices(BaseServices):

    def __init__(self, folder_path: str, file_name: str) -> None:
        super().__init__(folder_path, file_name)
        self._table_state: str = ''
        self._list_values: pd.DataFrame = None
        self.prepare_data()

    @property
    def table_state(self) -> str:
        return self._table_state

    @table_state.setter
    def table_state(self, table_state_value: str) -> None:
        self._table_state = table_state_value

    @property
    def list_values(self) -> pd.DataFrame:
        return self._list_values

    @list_values.setter
    def list_values(self, list_values: List[dict]) -> None:
        self._list_values = list_values

    def prepare_data(self) -> None:
        self.create_table()
        self._list_values = self.features_service.find_all(self._table_state,
                                                                       [STATE_FIELD_ID, STATE_FIELD_UF])

    def create_table(self) -> None:
        self._table_state = self.features_service.excel_to_table(
            self.configs['excel_states'],
            self.configs['workspace'],
            FEATURE_STATE,
            SHEET_NAME_STATE)

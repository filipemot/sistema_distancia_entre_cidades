from typing import List

import pandas as pd

from models.models_base import ModelsBase
from models.state import State
from utils.constants import FEATURE_CITY, SHEET_NAME_CITY, FIELD_STATE, FIELD_CITY_ID


class City(ModelsBase):

    def __init__(self, folder_path: str, file_name: str, state: State) -> None:
        super().__init__(folder_path, file_name)
        self.state: State = state
        self.table_city: str = None
        self._list_values: pd.DataFrame = None
        self.prepare_data()

    @property
    def list_values(self) -> pd.DataFrame:
        return self._list_values

    @list_values.setter
    def list_values(self, list_values: List[dict]) -> None:
        self._list_values = list_values

    def prepare_data(self) -> None:
        self.create_table()
        self.features_service.add_field_in_table(self.table_city, FIELD_STATE, 'Text')
        self.features_service.add_computed_field(self.table_city, FIELD_CITY_ID, '!OBJECTID!')

    def create_table(self) -> None:
        self.table_city = self.features_service.excel_to_table(
            self.configs['excel_city'], 
            self.configs['workspace'], 
            FEATURE_CITY,
            SHEET_NAME_CITY)

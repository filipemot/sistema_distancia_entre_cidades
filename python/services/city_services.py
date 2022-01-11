from typing import List

import arcpy  # type: ignore
import pandas as pd  # type: ignore

from services.base_services import ServicesBase
from services.state_services import StateServices
from utils.constants import FEATURE_CITY, SHEET_NAME_CITY, FIELD_STATE, FIELD_CITY_ID, FIELD_CITY_ID_STATE, \
    STATE_FIELD_ID, STATE_FIELD_UF, FEATURE_CITY_POINT, FIELD_CITY_LAT, FIELD_CITY_LNG, FIELD_CITY_LNG_STR, \
    FIELD_CITY_LAT_STR, FIELD_CITY_OBJECT_ID, TYPE_TEXT, TYPE_DOUBLE, TYPE_FLOAT


class CityServices(ServicesBase):

    def __init__(self, folder_path: str, file_name: str, state: StateServices) -> None:
        super().__init__(folder_path, file_name)
        self.state: StateServices = state
        self.table_city: str = ''
        self._list_values: pd.DataFrame = pd.DataFrame()
        self.table_city_geo = self.configs['workspace'] + "\\" + FEATURE_CITY_POINT
        self.prepare_data()

    @property
    def list_values(self) -> pd.DataFrame:
        return self._list_values

    @list_values.setter
    def list_values(self, list_values: List[dict]) -> None:
        self._list_values = list_values

    def save_field_state(self) -> None:
        cursor: arcpy.da.UpdateCursor = self.features_service.update_values(self.table_city,
                                                                            [FIELD_CITY_ID_STATE, FIELD_STATE])
        for row in cursor:
            state_row = self.state.list_values.loc[self.state.list_values[STATE_FIELD_ID] == row[0]]
            row[1] = state_row[STATE_FIELD_UF].values[0]
            cursor.updateRow(row)
        del cursor

    def add_fields_in_table(self) -> None:
        self.features_service.add_field_in_table(self.table_city, FIELD_STATE, TYPE_TEXT)
        self.features_service.add_computed_field(self.table_city, FIELD_CITY_ID, f'!{FIELD_CITY_OBJECT_ID}!', TYPE_TEXT)
        self.features_service.add_computed_field(self.table_city, f'{FIELD_CITY_LAT}',
                                                 f'{TYPE_FLOAT}(!{FIELD_CITY_LNG_STR}!)', TYPE_DOUBLE)
        self.features_service.add_computed_field(self.table_city, f'{FIELD_CITY_LNG}',
                                                 f'{TYPE_FLOAT}(!{FIELD_CITY_LAT_STR}!)', TYPE_DOUBLE)

    def prepare_data(self) -> None:
        self.create_table()
        self.add_fields_in_table()
        self.save_field_state()
        self.features_service.convert_table_to_point(self.table_city, self.table_city_geo,
                                                     FIELD_CITY_LAT, FIELD_CITY_LNG)

    def create_table(self) -> None:
        self.table_city = self.features_service.excel_to_table(
            self.configs['excel_city'],
            self.configs['workspace'],
            FEATURE_CITY,
            SHEET_NAME_CITY)

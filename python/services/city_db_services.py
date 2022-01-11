from typing import List

import psycopg2

from models.city import City
from services.db_services import DbServices
from utils.constants import TABLE_CITY_POSTGRESQL, FIELD_CITY_ID_POSTGREE, FIELD_CITY_NAME_POSTGREE, \
    FIELD_CITY_ID_REFERENCE_POSTGREE, FIELD_CITY_CODE_IBGE_POSTGREE, FIELD_CITY_LAT_POSTGREE, FIELD_CITY_LNG_POSTGREE, \
    FIELD_CITY_CAPITAL_POSTGREE, FIELD_CITY_STATE_POSTGREE, FIELD_CITY_CODE_PHONE_POSTGREE


class CityDbServices:

    def __init__(self):
        self.db_services: DbServices = DbServices()

    def delete_all_cities(self):
        cursor = self.db_services.conn.cursor()
        cursor.execute(f'DELETE FROM {TABLE_CITY_POSTGRESQL} WHERE 1=1')
        self.db_services.commit()
        cursor.close()

    def insert_cities(self, city_list: List[City]):
        cursor = self.db_services.conn.cursor()
        sql = f'INSERT INTO public.{TABLE_CITY_POSTGRESQL} ' \
              f'({FIELD_CITY_ID_POSTGREE}, {FIELD_CITY_NAME_POSTGREE}, {FIELD_CITY_ID_REFERENCE_POSTGREE}, ' \
              f'{FIELD_CITY_CODE_IBGE_POSTGREE}, {FIELD_CITY_LAT_POSTGREE}, {FIELD_CITY_LNG_POSTGREE}, ' \
              f'{FIELD_CITY_CAPITAL_POSTGREE}, {FIELD_CITY_STATE_POSTGREE}, {FIELD_CITY_CODE_PHONE_POSTGREE}) VALUES '

        values = self.get_values_insert(city_list, cursor)

        cursor.execute(f'{sql} {values}')
        self.db_services.commit()
        cursor.close()

    @staticmethod
    def get_values_insert(city_list: List[City], cursor: psycopg2.extensions.cursor) -> str:
        tuple_values = []

        for city in city_list:
            tuple_values.append((city.id_city, city.name, city.id_reference, city.ibge_code, city.lat, city.lng,
                                 str(city.capital), city.state, city.phone_code))

        return ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in tuple_values)
from services.db_services import DbServices
from utils.constants import TABLE_CITY_POSTGRESQL


class CityDbServices:

    def __init__(self):
        self.db_services: DbServices = DbServices()

    def delete_all_cities(self):
        cursor = self.db_services.conn.cursor()
        cursor.execute(f'DELETE FROM {TABLE_CITY_POSTGRESQL}')

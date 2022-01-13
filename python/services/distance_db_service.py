from services.db_services import DbService
from utils.constants import TABLE_DISTANCE_POSTGRESQL


class DistanceDbService:

    def __init__(self):
        self.db_services: DbService = DbService()

    def delete_all_distances(self):
        cursor = self.db_services.conn.cursor()
        cursor.execute(f'DELETE FROM {TABLE_DISTANCE_POSTGRESQL} WHERE 1=1')
        self.db_services.commit()
        cursor.close()

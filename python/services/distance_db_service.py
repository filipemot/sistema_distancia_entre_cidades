from models.distance import Distance
from services.db_services import DbService
from utils.constants import TABLE_DISTANCE_POSTGRESQL, FIELD_DISTANCE_TABLE_POSTGREE, FIELD_DISTANCE_ID_POSTGREE, \
    FIELD_DISTANCE_ID_ORIGIN_POSTGREE, FIELD_DISTANCE_ID_DESTINATION_POSTGREE, FIELD_DISTANCE_MINUTES_POSTGREE, \
    FIELD_DISTANCE_TRAVEL_TIME_POSTGREE, FIELD_DISTANCE_MILES_POSTGREE, FIELD_DISTANCE_KILOMETER_POSTGREE, \
    FIELD_DISTANCE_TIME_AT_POSTGREE, FIELD_DISTANCE_WALK_TIME_POSTGREE, FIELD_DISTANCE_TRUCK_TIME_POSTGREE, \
    FIELD_DISTANCE_TRAVEL_TRUCK_TIME_POSTGREE


class DistanceDbService:

    def __init__(self):
        self.db_services: DbService = DbService()

    def delete_all_distances(self):
        cursor = self.db_services.conn.cursor()
        cursor.execute(f'DELETE FROM {TABLE_DISTANCE_POSTGRESQL} WHERE 1=1')
        self.db_services.commit()
        cursor.close()

    def insert_distances(self, distance: Distance):
        cursor = self.db_services.conn.cursor()
        sql = f'INSERT INTO public.{FIELD_DISTANCE_TABLE_POSTGREE} ' \
              f'({FIELD_DISTANCE_ID_POSTGREE}, ' \
              f'{FIELD_DISTANCE_ID_ORIGIN_POSTGREE}, ' \
              f'{FIELD_DISTANCE_ID_DESTINATION_POSTGREE}, ' \
              f'{FIELD_DISTANCE_MINUTES_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRAVEL_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_MILES_POSTGREE}, ' \
              f'{FIELD_DISTANCE_KILOMETER_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TIME_AT_POSTGREE}, ' \
              f'{FIELD_DISTANCE_WALK_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRUCK_TIME_POSTGREE}, ' \
              f'{FIELD_DISTANCE_TRAVEL_TRUCK_TIME_POSTGREE}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'

        cursor.execute(f'{sql}', (
            distance.id_distance,
            distance.id_city_origin,
            distance.id_city_destiny,
            distance.minutes,
            distance.travel_time,
            distance.miles,
            distance.kilometers,
            distance.time_at,
            distance.walk_time,
            distance.truck_time,
            distance.travel_truck_time,
        ))
        self.db_services.commit()
        cursor.close()

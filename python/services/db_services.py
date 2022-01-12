import logging

import psycopg2  # type: ignore

from services.config_db_service import ConfigDbService


class DbService:

    def __init__(self):
        self.conn = None
        self.config_db_service = ConfigDbService()
        self.connect()

    def connect(self):
        try:
            params = self.config_db_service.config()

            self.conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.conn = None

    def close_connection(self) -> None:
        if self.conn is not None:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def __del__(self) -> None:
        self.close_connection()

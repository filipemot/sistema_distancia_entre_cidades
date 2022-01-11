import logging

import psycopg2  # type: ignore

from services.config_services import config


class DbServices:

    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            params = config()

            self.conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.conn = None

    def close_connection(self) -> None:
        if self.conn is not None:
            self.conn.close()

    def __del__(self) -> None:
        self.close_connection()

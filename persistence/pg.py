import os
import psycopg2
import logging

logger_work = logging.getLogger("work")

PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "password")
PG_HOST = os.getenv("POSTGRES_HOST", "192.168.99.100")
PG_PORT = os.getenv("POSTGRES_PORT", 5432)
PG_DATABASE = os.getenv("POSTGRES_DATABASE", "ml_data")
ITEM_TABLE = os.getenv("ITEM_TABLE", "items")


class Pg:
    """ Postgres presistence implementation """
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user=PG_USER,
                                               password=PG_PASS,
                                               host=PG_HOST,
                                               port=PG_PORT,
                                               database=PG_DATABASE)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            logger_work.error(error)

        self.fields = (
            "site",
            "id",
            "price",
            "start_time",
            "name",
            "description",
            "nickname"
        )

    def __del__(self):
        self.connection.close()

    def __none_to_empty(self, value):
        return value if value else ""

    def __spread_data(self, item: dict) -> tuple:
        return tuple(
            self.__none_to_empty(item.get(field))
            for field in self.fields)

    def __make_line_sql(self, item: dict) -> str:
        field_names = ",".join(self.fields)
        line_sql = f"INSERT INTO {ITEM_TABLE} ({field_names}) VALUES {self.__spread_data(item)};\n"  # noqa
        return line_sql

    def write_rows(self, data: list) -> str:
        sql = ""
        for item in data:
            if item:
                sql += self.__make_line_sql(item)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            logger_work.error(f"Cannot write data to PG.\n{e}")

    def read_row(self, pk: str) -> dict:
        print(f"reading {pk} from postgres")
        return {"data": "fake"}

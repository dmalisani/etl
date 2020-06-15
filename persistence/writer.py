from persistence.pg import Pg
import logging

logger_work = logging.getLogger("work")

try:
    db = Pg()  # You can implement another engine writer
except Exception as e:
    logger_work.error(f"Cannot connecto to PG\n{e}")
    db = None


def write_rows(data_row: dict) -> str:
    return db.write_rows(data_row)

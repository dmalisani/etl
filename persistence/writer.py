from persistence.pg import Pg

db = Pg()  # You can implement another engine writer


def write_rows(data_row: dict) -> str:
    return db.write_rows(data_row)

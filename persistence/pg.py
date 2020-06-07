from uuid import uuid4


class Pg:
    """ Postgres presistence implementation """

    def write_row(self, data: dict) -> str:
        print(f"write {data} in postgres db")
        return str(uuid4())

    def read_row(self, pk: str) -> dict:
        print(f"reading {pk} from postgres")
        return {"data": "fake"}

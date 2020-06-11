from data_processor.api_conector import (
    get_items, get_category_name, get_currency_description, get_nickname)
from concurrent.futures import ThreadPoolExecutor
import re


def _valid_item(item: dict) -> bool:
    there_is_error = item.get("body", {}).get("error", False)
    return not there_is_error


def _split_id(mixed_id: str) -> tuple:
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    find = r.match(mixed_id)
    return find.groups()


def data_extractor(batch_data: list) -> list:
    ids = [
        "{0}{1}".format(row['site'], row['id']) for row in batch_data
        ]
    row_items = get_items(ids)
    refined_items = complete_and_purge(row_items)
    return refined_items


def complete_and_purge(items: list) -> dict:
    task_items = []

    with ThreadPoolExecutor(20) as list_executor:
        task_items = [list_executor.submit(fill_item, item) for item in items]

    return [task.result() for task in task_items]


def fill_item(item):
    if not _valid_item(item):
        return {}

    root_item = item.get('body')
    new_item = {
        "site": root_item.get("site_id"),
        "id": _split_id(root_item.get("id"))[1],
        "start_time": root_item.get("start_time"),
        "price": root_item.get("price"),
    }
    with ThreadPoolExecutor(3) as fill_item_executor:
        t_nickname = fill_item_executor.submit(
            get_nickname, root_item.get("seller_id"))
        t_description = fill_item_executor.submit(
            get_currency_description, root_item.get("currency_id"))
        t_category = fill_item_executor.submit(
            get_category_name, root_item.get("category_id"))

        new_item.update(
            {
                "name": t_category.result(),
                "description": t_description.result(),
                "nickname": t_nickname.result()
            }
        )
    return new_item

import os
import requests
import logging
import time

logger_perf = logging.getLogger("performance")
logger_work = logging.getLogger("work")

BASE_URL = os.getenv("MELI_API_BASE_URL", "https://api.mercadolibre.com")


def get_items(list_of_id: list) -> dict:

    time_start = time.perf_counter()
    if not len(list_of_id) or len(list_of_id) > 20:
        logger_work.warning("Api of items called with wrong list of ids")
        return {}
    ids_str = ",".join(list_of_id)
    url = f"{BASE_URL}/items?ids={ids_str}"
    try:
        response = requests.get(url)
        logger_perf.debug("Process {0}".format(
                round(time.perf_counter() - time_start, 2)))
        return response.json()
    except Exception as e:
        logger_work.error(f"Cannot parse response\n{e}")
        return {}


def get_category_name(id_category: str) -> str:
    url = f"{BASE_URL}/categories/{id_category}"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        logger_work.error(f"Cannot parse response\n{e}")
        return None
    return data.get("name")


def get_currency_description(id_currency: str) -> str:
    url = f"{BASE_URL}/currencies/{id_currency}"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        logger_work.error(f"Cannot parse response\n{e}")
        return None
    return data.get("description")


def get_nickname(id_user: str) -> str:
    url = f"{BASE_URL}/users/{id_user}"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        logger_work.error(f"Cannot parse response\n{e}")
        return None
    return data.get("nickname")

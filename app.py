from flask import Flask
from concurrent.futures import ThreadPoolExecutor
from data_processor.manager import digest_data

import logging
import pathlib
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)
executor = ThreadPoolExecutor(thread_name_prefix="etl_")

SAMPLE_DATA = str(pathlib.Path(__file__).parent.joinpath("data.csv"))


@app.route('/')
def sample():
    lauched_thread = executor.submit(digest_data, SAMPLE_DATA)
    lauched_thread.add_done_callback()


    return 'ETL Sample is working'

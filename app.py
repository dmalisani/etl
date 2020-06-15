import os
import logging
import pathlib
import sys
from flask import Flask
from concurrent.futures import ThreadPoolExecutor
from data_processor.manager import digest_data

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
SAMPLE_DATA = str(pathlib.Path(__file__).parent.joinpath("data.csv"))
logger_work = logging.getLogger("work")


def create_app():
    app = Flask(__name__)
    executor = ThreadPoolExecutor(thread_name_prefix="etl_")

    @app.route('/')
    def home():
        return 'ETL it works. Click <a href="./run">here</a> to run it'

    @app.route('/run')
    def sample():
        logger_work.info("Starting job with {0}".format(repr(SAMPLE_DATA)))
        executor.submit(digest_data, SAMPLE_DATA)
        return 'ETL Sample is working'
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
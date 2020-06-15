from flask import Flask
from concurrent.futures import ThreadPoolExecutor
from data_processor.manager import digest_data

import logging
import pathlib
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
SAMPLE_DATA = str(pathlib.Path(__file__).parent.joinpath("data.csv"))


def create_app():
    app = Flask(__name__)
    executor = ThreadPoolExecutor(thread_name_prefix="etl_")

    @app.route('/')
    def home():
        return 'ETL it works. Click <a href="./run">here</a> to run it'

    @app.route('/run')
    def sample():
        executor.submit(digest_data, SAMPLE_DATA)
        return 'ETL Sample is working'
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
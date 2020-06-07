from flask import Flask
from data_processor import manager
from concurrent.futures import ThreadPoolExecutor
from data_processor.manager import digest_data

app = Flask(__name__)
executor = ThreadPoolExecutor()

@app.route('/')
def hello_world():
    executor.submit(digest_data, "current_path")
    return 'ETL Sample is working'

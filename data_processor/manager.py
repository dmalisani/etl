import os
import logging
import time
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from data_parser.csv_parser import reader
from persistence.writer import write_rows
from data_processor.get_data import data_extractor

logger_perf = logging.getLogger("performance")
logger_work = logging.getLogger("work")

BATCH_SIZE = os.getenv("REQUEST_BATCH_SIZE", 20)
PARALLEL_PROCESSES = cpu_count()


def valid_data(row_data: list) -> dict:
    row_parsed = {}
    try:
        assert len(row_data[0]) == 3
        assert row_data[1].isnumeric()
        row_parsed = {"site": row_data[0], "id": row_data[1]}
    except Exception:
        pass
    return row_parsed


def process_line(row_data):
    time_start = time.perf_counter()
    extracted_data = data_extractor(row_data)
    logger_perf.debug("Process {0}".format(
                    round(time.perf_counter() - time_start, 2)))
    return extracted_data


def store_batch(task):
    with ThreadPoolExecutor() as thread_writer:
        thread_writer.submit(write_rows, task.result())


def digest_data(file_path: str):

    time_start = time.perf_counter()
    logger_work.info(f"Processing {file_path}")

    data_reader = reader(file_path)
    count = 0
    data_count = 0
    with ProcessPoolExecutor(PARALLEL_PROCESSES) as executor:
        data_available = True
        while data_available:
            batch = []
            for _ in range(BATCH_SIZE):
                try:
                    data_line = next(data_reader)
                    data = valid_data(data_line)
                    if data:
                        batch.append(data)
                        data_count += 1
                except StopIteration:
                    data_available = False

            if batch:
                task = executor.submit(process_line, batch)
                task.add_done_callback(store_batch)
                count += 1
            else:
                logger_work.warning("Cannot make key for {0}".format(
                    repr(data_line)))

            # DEBUG
            # if count > 2:
            #     break
    work_time = round(time.perf_counter() - time_start, 2)
    logger_perf.debug("Execution of {1} records took {0}".format(
                    work_time,
                    data_count))
    logger_perf.info(f"Job in {file_path} done in {work_time} secs.")

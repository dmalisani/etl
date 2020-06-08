import logging
import time
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from data_parser.csv_parser import reader

logger_perf = logging.getLogger("performance")
logger_work = logging.getLogger("work")


def make_key(data):
    key = None
    try:
        assert len(data[0]) == 3
        assert data[1].isnumeric()
        key = "{0}{1}".format(data[0], data[1])
    except Exception:
        pass
    return key


def process_line(row_data):
    time_start = time.perf_counter()
    time.sleep(3)
    logger_perf.debug("Process {0}".format(
                    round(time.perf_counter() - time_start, 2)))
    return "proc data {0}".format(row_data)


def store_line(task):
    logger_work.info("Storing data: {0}".format(task.result()))


def digest_data(file_path: str):

    time_start = time.perf_counter()
    logger_work.info(f"Processing {file_path}")

    data = reader(file_path)
    count = 0
    with ProcessPoolExecutor(cpu_count()) as executor:
        for data_line in data:
            key = make_key(data_line)
            if key:
                task = executor.submit(process_line, key)
                task.add_done_callback(store_line)
            else:
                logger_work.warning("Cannot make key for {0}".format(
                    repr(data_line)))

            # DEBUG
            count += 1
            if count == 10:
                break

    logger_perf.debug("Execution of {1} records took {0}".format(
                    round(time.perf_counter() - time_start, 2),
                    count))
    logger_perf.info(f"Job in {file_path} done")

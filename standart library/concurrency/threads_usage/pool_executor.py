import time
from concurrent.futures import ThreadPoolExecutor


threads = 4


def _import_listing(self, item):
    pass


if __name__ == "__main__":

    start_time = time.time()

    executor = ThreadPoolExecutor(max_workers=threads)

    for item in range(100):
        executor.submit(_import_listing, item)

    executor.shutdown()

    duration = time.time() - start_time
    print(duration)

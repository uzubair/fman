import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


log = logging.getLogger("i.task")


class TaskManager(object):

    max_workers = 10

    def __init__(self, options):
        self.options = options


    def execute(self):
        log.info(f"Distributing tasks to a maximum of {TaskManager.max_workers} workers")
        with ThreadPoolExecutor(max_workers=TaskManager.max_workers) as executor:
            futures = []
            for path in self.options.path:
                futures.append(executor.submit(self.options.func, path, self.options))
            for future in as_completed(futures):
                try:
                    _path, files = future.result()
                    self.display_results(_path, files)
                except Exception as e:
                    log.info(f"An error occurred processing {path}: {e}")


    def display_results(self, path, files):
        log.info(f"\nFound {len(files)} files in {path}")
        for file in files:
            log.info(f" - {file}")
        log.info("")
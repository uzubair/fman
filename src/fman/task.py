import logging
from queue import Queue
from threading import Thread

log = logging.getLogger("i.task")


class ThreadPoolWorker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # an exception happend in this thread
                print(e)
            finally:
                # make this task as done, whether an
                # exception happend or not
                self.tasks.task_done()


class ThreadPoolManager():
    """ Manages pool of threads consuming tasks from a queue """
    def __init__(self, num_threads=5):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            ThreadPoolWorker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for the completion of all the tasks in the queue """
        self.tasks.join()

import atexit
import logging.config
import os
import threading
import queue
from concurrent.futures.thread import _python_exit
from datetime import time
from time import sleep

import yaml
from kazoo.client import KazooClient

from executor.executor import Executor, MockZKClient, MockScheduler

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    executor = Executor()

    atexit.unregister(_python_exit)

    def print_trigger(trigger):
        print("in callback %s" % trigger)

    # trigger job
    executor.trigger(1, 1, "HelloJob", "unittest.job.HelloJob", {}, print_trigger)
    executor.trigger(2, 2, "HelloJobTwo", "unittest.job.HelloJobTwo", {"secs": 10, "name": "shuzai"}, print_trigger)
    executor.trigger(3, 3, "HelloJobThree", "unittest.job.HelloJobThree", {}, print_trigger)

    # def interrupt():
    #     print("about to interrupt 3")
    #     executor.interrupt(3)
    #
    # threading.Timer(5, interrupt).start()

    # executor.trigger(4, 4, "HelloJobTwo", "job.HelloJobTwo", {"secs": 10, "name": "maomi"})

    # sleep(30)
    executor.shutdown(timeout=15)
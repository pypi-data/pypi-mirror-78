import datetime
import logging.config
import os
import random
import threading
import time
from time import sleep

import yaml

from executor.notifier import _Timer, ExponentialRetryStrategy

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    def fn():
        print("%s in fn" % datetime.datetime.now())

    def fn2():
        if random.random() > 0.1:
            raise RuntimeError("intentional error")
        print("%s in fn2" % datetime.datetime.now())

    timer = _Timer(ExponentialRetryStrategy(init_interval=1, max_interval=10))
    timer.start()
    timer.schedule(1, fn2)
    sleep(100)
    stopped = timer.shutdown(15)
    print(stopped)
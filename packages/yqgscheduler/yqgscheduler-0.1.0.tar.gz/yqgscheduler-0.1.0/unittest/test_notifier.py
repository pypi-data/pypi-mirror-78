import datetime
import logging.config
import os
import random
from time import sleep

import yaml

from executor.notifier import ExponentialRetryStrategy, _Timer

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/../logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    def fn():
        print("%s in fn" % datetime.datetime.now())

    def fn2():
        if random.random() > 0.1:
            raise RuntimeError("intentional error")
        print("%s in fn2" % datetime.datetime.now())

    def fn3(secs):
        print("about to sleep %s seconds" % secs)
        sleep(secs)
        print("%s in fn2" % datetime.datetime.now())

    timer = _Timer(ExponentialRetryStrategy(init_interval=1, max_interval=10))
    timer.start()
    timer.schedule(0, fn)
    timer.schedule(1, fn)
    timer.schedule(2, fn)
    timer.schedule(3, fn)
    timer.schedule(4, fn)
    timer.schedule(5, fn)
    sleep(10)
    stopped = timer.shutdown(5)
    print(stopped)
import logging.config
import os

import yaml

from kazoo.client import KazooClient

from executor.app import ExecutorApplication
from executor.executor import Executor
from executor.notifier import MockNotifier
from executor.scheduler import Scheduler

if __name__ == '__main__':
    import sys

    print(sys.path)

    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    # initialize components
    zk = KazooClient(hosts='127.0.0.1:2181')
    executor = Executor()
    scheduler = Scheduler()
    notifier = MockNotifier()

    # initialize executor & remote yqg-scheduler
    app = ExecutorApplication("yqg-qa#localhost:8080", zk, executor, scheduler, notifier)

    # register shutdown hook
    # def graceful_shutdown():
    #     app.shutdown(timeout=60)
    #
    # atexit.unregister(_python_exit)
    # atexit.register(graceful_shutdown)

    app.start()

    # remote_epoch, trigger_id, job_id, name, class_name, params=None
    trigger1 = app.trigger(54, 1, 1, "HelloJob1", "unittest.job.HelloJob")
    trigger2 = app.trigger(54, 2, 2, "HelloJob2", "unittest.job.HelloJobTwo", {"secs": 10, "name": "maomi"})
    trigger3 = app.trigger(54, 3, 3, "HelloJob3", "unittest.job.HelloJobThree", {"name": "shuzai"})
    # def interrupt():
    #     app.interrupt(54, 1)
    # Timer(5, interrupt).start()
    triggers = app.list_triggers(54)
    for trigger in triggers:
        print("%s" % trigger)
    trigger = app.list_triggers(54, trigger_id=3)

    app.shutdown(timeout=60)

import json
import logging.config
import os
from threading import Timer

import yaml
from kazoo.protocol.states import ZnodeStat

from executor.scheduler import Scheduler

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    metadata = {
        "address": "172.20.64.12:7039",
        "epoch": 54,
        "timeUpdated": 1594102627167
    }

    scheduler = Scheduler()
    scheduler.update_metadata(json.dumps(metadata).encode("utf-8"), ZnodeStat(1,1,1,1,1,1,1,1,1,1,1))
    print(scheduler.metadata())

    def update_metadata():
        metadata = {
            "address": "172.20.64.12:7039",
            "epoch": 55,
            "timeUpdated": 1694102627167
        }
        scheduler.update_metadata(json.dumps(metadata).encode("utf-8"), ZnodeStat(1,1,1,1,1,1,1,1,1,1,1))

    Timer(10, update_metadata).start()

    scheduler.await_metadata(55, timeout=15)

    print(scheduler.metadata())
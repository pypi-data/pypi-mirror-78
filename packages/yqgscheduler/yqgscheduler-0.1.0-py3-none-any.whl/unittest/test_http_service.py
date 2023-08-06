import atexit
import logging
import logging.config
import os
from concurrent.futures.thread import _python_exit

import requests
import yaml

from kazoo.client import KazooClient

from executor.app import ExecutorApplication
from executor.httpservice import HttpService

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    dir = os.path.dirname(full_path)
    with open("%s/logging.yaml" % dir, 'rt') as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    # initialize http service
    service = HttpService("yqg-qa", {"http.port": 8081})

    service.serve()

    # register shutdown hook
    def graceful_shutdown():
        service.shutdown()

    atexit.unregister(_python_exit)
    atexit.register(graceful_shutdown)

    requests.post()

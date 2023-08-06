import logging
from time import sleep

from executor.job import Job


class HelloJob(Job):

    def run(self, **params):
        logging.info("hello world")


class HelloJobTwo(Job):

    def run(self, **params):
        name = params["name"]
        secs = params["secs"]
        sleep(secs)
        logging.info("hello %s" % name)


class HelloJobThree(Job):

    def run(self, **params):
        while not self.is_interrupted():
            logging.info("not interrupted")
            sleep(1)
        logging.info("interrupted...")
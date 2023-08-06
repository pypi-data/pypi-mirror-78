import logging
import time

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
from kazoo.recipe.watchers import DataWatch


def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print("lost...")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print("suspended...")
    else:
        # Handle being connected/reconnected to Zookeeper
        print("else...")


def your_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print("lost...")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print("suspended...")
    else:
        # Handle being connected/reconnected to Zookeeper
        print("else...")

def hello(**params):
    print("hello")


if __name__ == '__main__':
    logger = logging.getLogger('py-yqg-scheduler')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    zk = KazooClient(hosts='127.0.0.1:2181', timeout=5)

    def connection_listener(state):
        logger.info("connection listener %s" % state)

    zk.add_listener(connection_listener)

    # # add watcher
    # def get_zk(value, stat):
    #     logger.info("zk value change %s" % value)
    #
    # def watcher(event):
    #     logger.info(event)
    #     zk.get("/dist_scheduler/executor/localhost:9090", watch=watcher)
    #
    # #zk.get("/dist_scheduler/executor/localhost:9090", watch=watcher)
    # DataWatch(zk, "/dist_scheduler/executor/localhost:9090", get_zk)


    zk.start()

    time.sleep(1000)
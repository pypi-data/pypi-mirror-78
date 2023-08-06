from abc import abstractmethod


class Job(object):

    def __init__(self):
        self._interrupted = False

    @abstractmethod
    def run(self, **params):
        pass

    def interrupt(self):
        self._interrupted = True

    def is_interrupted(self):
        return self._interrupted


class JobFactory(object):

    @abstractmethod
    def create(self, class_name):
        """
        :param class_name: 类名称
        :return: job实例
        """
        pass

import abc
import inspect
import time

from . import msg


class ISubscriber(metaclass=abc.ABCMeta):
    _SUBSCRIBE_ACTION_NAME = "subscribe"

    @abc.abstractmethod
    def subscribe(self, *args, **kwargs):
        raise NotImplementedError("subscribe must be imlplemented in subclass")


class DefaultSubscriber(
    ISubscriber
):

    def subscribe(self, msg: object):
        print(msg)
        raise NotImplementedError(f"subscribe must be implemented in subclass of DefaultSubscriber")


class AConcreteObserver(DefaultSubscriber):

    def subscribe(self, msg: msg.DictMessage):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")


class BConcreteObserver(DefaultSubscriber):

    def subscribe(self, msg: msg.IntMessage):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")


class CConcreteObserver(DefaultSubscriber):

    def subscribe(self, msg: msg.IntMessage):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")

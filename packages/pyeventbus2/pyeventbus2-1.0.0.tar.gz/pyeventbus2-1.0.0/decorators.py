import functools
import logging
import time
import types
from typing import Dict, List
from . import subscriber


def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        logging.info(
            "func:{} call took {} ms".format(func.__name__, (end - start) * 1000)
        )
        print("func:{} call took {} ms".format(func.__name__, (end - start) * 1000))
        return res

    return wrapper


def validate_observer(func: types.MethodType) -> types.FunctionType:
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        self, observer = args
        if not issubclass(observer.__class__, subscriber.DefaultSubscriber):
            raise NotImplementedError(f"{observer} must be subclass of {subscriber.DefaultSubscriber}")

        if not self._ObserverRegistry__finder.find_method(
                subscriber.DefaultSubscriber.subscribe.__name__,
                observer.__class__
        ):
            raise NotImplementedError(
                f"{subscriber.DefaultSubscriber.subscribe.__name__} must be implemented in {observer.__class__}")

        return func(*args, **kwargs)

    return decorator


def validate_observer_from_config(func: types.MethodType) -> types.FunctionType:
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        self, config_observer_registry = args
        for item in config_observer_registry:
            for observers in item.values():
                for observer in observers:
                    if not issubclass(observer.__class__, subscriber.DefaultSubscriber):
                        raise NotImplementedError(f"{observer} must be subclass of {subscriber.DefaultSubscriber}")

                    if not self._ObserverRegistry__finder.find_method(
                            subscriber.DefaultSubscriber.subscribe.__name__,
                            observer.__class__
                    ):
                        raise NotImplementedError(
                            f"{subscriber.DefaultSubscriber.subscribe.__name__} must be implemented in {observer.__class__}")
        return func(*args, **kwargs)

    return decorator

# def is_subclass_of_subscriber(func: types.MethodType) -> types.FunctionType:
#     @functools.wraps(func)
#     def decorator(*args, **kwargs):
#         self, clazz = args
#         if not issubclass(clazz, subscriber.DefaultSubscriber):
#             raise NotImplementedError(f"{clazz} must be subclass of {subscriber.DefaultSubscriber}")
#         return func(*args, **kwargs)
#
#     return decorator
#
#
# def subscribe(func: types.MethodType) -> types.FunctionType:
#     @functools.wraps(func)
#     def decorator(*args, **kwargs):
#         self, event = args
#         a_tuple = (Dict,)
#         if not issubclass(event, a_tuple):
#             raise NotImplementedError(f"{event} must be subclass of {a_tuple}")
#         return func(*args, **kwargs)
#
#     return decorator


# def validate_observers(func: types.MethodType) -> types.FunctionType:
#     @functools.wraps(func)
#     def decorator(*args, **kwargs):
#         _, observers = args
#         if not isinstance(observers, List):
#             raise Exception(f"{observers} must be list")
#         for observer in observers:
#             if not isinstance(observer, subscriber.DefaultSubscriber):
#                 raise NotImplementedError(f"{observer} must be subclass of {subscriber.DefaultSubscriber}")
#         return func(*args, **kwargs)
#
#     return decorator


# def validate_object(func: types.MethodType) -> types.FunctionType:
#     @functools.wraps(func)
#     def decorator(*args, **kwargs):
#         _, observer = args
#         if not isinstance(observer, subscriber.DefaultSubscriber):
#             raise NotImplementedError(f"{observer} must be subclass of {subscriber.DefaultSubscriber}")
#
#         return func(*args, **kwargs)
#
#     return decorator

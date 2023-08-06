from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import NoReturn, List
from pyeventbus import conf
from pyeventbus import executors, decorators
from pyeventbus.registry import ObserverRegistry


class EventBus():

    def __init__(self, executor: ThreadPoolExecutor = executors.DefaultExecutor(),
                 config_observer_registry: list = conf.OBSERVER_REGISTRY):
        assert isinstance(executor, ThreadPoolExecutor), f"{executor} must be subclass of {ThreadPoolExecutor}"
        self.__executor = executor
        self.__observer_registry = ObserverRegistry(config_observer_registry)

    # @decorators.validate_object
    def register(self, object: object) -> NoReturn:
        self.__observer_registry.register(object)

    def notify(self, event: object) -> NoReturn:
        _observer_actions = self.__observer_registry.get_matched_observer_actions(event)
        with self.__executor as executor:
            all_task = [executor.submit(action.do_execute, (event)) for action in _observer_actions]

            for future in as_completed(all_task):
                data = future.result()
                print(f"{data}")

    # def notify2(self, observer_actions: List[ObserverAction], event: object) -> NoReturn:
    #     with self.__executor as executor:
    #         all_task = [executor.submit(action.do_execute, (event)) for action in observer_actions]
    #
    #         for future in as_completed(all_task):
    #             data = future.result()
    #             print(f"future: {data}")

    # def __str__(self):
    #     return f"{self.__class__}#notify"


class AsyncEventBus(EventBus):

    def __init__(self, executor: ThreadPoolExecutor = executors.DefaultExecutor(max_workers=5)):
        super(AsyncEventBus, self).__init__(executor)

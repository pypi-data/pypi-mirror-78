import copy
from typing import NoReturn, List, Dict

from pyeventbus import decorators, finder, conf
from pyeventbus.action import ObserverAction


class ObserverRegistry():
    __registry = {}

    def __init__(self, config_observer_registry: list = conf.OBSERVER_REGISTRY):
        self.__finder = finder.BlockFinderDecorator()
        self.__register_from_config(config_observer_registry)

    @decorators.validate_observer_from_config
    def __register_from_config(self, config_observer_registry):
        # copy_of_registry = {}

        for item in config_observer_registry:
            self.__registry.update(item)

        for msg_type, observers in self.__registry.items():
            observer_action_list = []
            for observer in observers:
                observer_action = self.find_all_observer_action(observer)
                if not observer_action.get(msg_type, None):
                    raise Exception(
                        f"observer_action: {observer_action.values()}'s key is not match with config'key: {msg_type}")
                observer_action_list.extend(observer_action.get(msg_type))
            self.__registry[msg_type] = observer_action_list

    # manually register observer which wants receive msg
    @decorators.validate_observer
    def register(self, observer: object) -> NoReturn:
        observer_action = self.find_all_observer_action(observer)
        for event_type, event_values in observer_action.items():
            if not self.__registry.get(event_type):
                self.__registry.setdefault(event_type, [])
            self.__registry[event_type].extend(event_values)

    def get_matched_observer_actions(self, event: object) -> List[ObserverAction]:
        matched_observers = []
        posted_event_type = event.__class__
        for event_type, event_value in self.__registry.items():
            if posted_event_type is event_type:
                matched_observers.extend(event_value)
        return matched_observers

    def find_all_observer_action(self, observer: object) -> Dict:
        observer_actions = {}
        _clazz = observer.__class__
        args_info = self.__finder.get_args(_clazz.subscribe)
        if not observer_actions.get(args_info.annotations['msg'], None):
            observer_actions.setdefault(args_info.annotations['msg'], [])
        observer_actions[args_info.annotations['msg']].append(ObserverAction(observer, "subscribe"))
        return observer_actions

    # def find_all_observer_actions(self, observer: object) -> Dict[Any, List[ObserverAction]]:
    #     observer_actions = {}
    #     _clazz = observer.__class__
    #     for method in self.get_annotated_methods(_clazz):
    #         observer_actions.append(ObserverAction(observer, method))
    #
    # # @decorators.is_subclass_of_subscriber
    # def get_annotated_methods(self, clazz: type) -> List[Optional[str]]:
    #     annotated_methods = []
    #     _list = self.__finder.is_decorated_by(decorators.subscribe.__name__, clazz)
    #     annotated_methods.extend(_list)
    #     return annotated_methods

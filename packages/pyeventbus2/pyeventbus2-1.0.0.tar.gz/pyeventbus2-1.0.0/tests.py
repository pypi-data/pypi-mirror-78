import time
import unittest
import inspect
from pyeventbus import subscriber, decorators, finder, registry, conf, eventbus, msg
from pyeventbus import action


class ASubscriber(subscriber.DefaultSubscriber):
    def subscribe(self, msg: msg.DictMessage):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")


class ConcreteSubscriber(subscriber.DefaultSubscriber):

    def subscribe(self, msg: object):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")


class TestConfig(unittest.TestCase):

    def test_observers(self):
        print(conf.OBSERVER_REGISTRY)


class TestSubscriber(unittest.TestCase):

    def test_init(self):
        _subscriber = subscriber.DefaultSubscriber()

    def test_default_subscriber_subscribe(self):
        _subscriber = subscriber.DefaultSubscriber()
        _subscriber.subscribe({"name": "jay"})

    def test_subclass_of_default_subscriber_subscribe(self):
        _subscriber = ConcreteSubscriber()
        _subscriber.subscribe({"name": "jay"})


class TestDecorator(unittest.TestCase):

    @decorators.log_execution_time
    def test_log_execute_time(self):
        time.sleep(2)


class TestFinder(unittest.TestCase):

    def test_find_method(self):
        _finder = finder.BlockFinderDecorator()
        res = _finder.find_method("subscribe", ConcreteSubscriber)
        assert res
        res = _finder.find_method("subscribe", ASubscriber)
        assert res, f"method: subscribe not found in {ASubscriber}"

    def test_get_args(self):
        _finder = finder.BlockFinderDecorator()
        res = _finder.get_args(ConcreteSubscriber.subscribe)
        print(res.annotations)


class TestObserverAction(unittest.TestCase):

    def test_do_execute(self):
        o_action = action.ObserverAction(ConcreteSubscriber(), "subscribe")
        o_action.do_execute({"name": "jay"})


class TestObserverRegistry(unittest.TestCase):

    def test_register(self):
        _as = ASubscriber()
        _registry = registry.ObserverRegistry()
        _registry.register(_as)

    def test_find_all_observer_action(self):
        _as = ASubscriber()
        _registry = registry.ObserverRegistry()
        _registry.register(_as)
        res = _registry.find_all_observer_action(_as)
        print(res)


class TestEventBus(unittest.TestCase):

    @decorators.log_execution_time
    def test_(self):
        # _msg = msg.DictMessage({"name": "jay"})
        # _as = ASubscriber()
        sync_event_bus = eventbus.AsyncEventBus()
        # sync_event_bus.notify(msg.DictMessage({"name": "jay"}))
        sync_event_bus.notify(msg.IntMessage(1211))
        # sync_event_bus.register(_as)
        # sync_event_bus.notify(_msg)

#
# class TestSetup(unittest.TestCase):
#
#     def test_md_2_rst(self):
#         # 将markdown格式转换为rst格式
#         def md_to_rst(from_file, to_file):
#             try:
#                 r = requests.post(
#                     url='http://c.docverter.com/convert',
#                     data={'to': 'rst', 'from': 'markdown'},
#                     files={'input_files[]': open(from_file, 'rb')}
#                 )
#                 if r.ok:
#                     with open(to_file, "wb") as f:
#                         f.write(r.content)
#
#             except Exception as e:
#                 print(str(e))
#
#         md_to_rst("README.md", "README.rst")

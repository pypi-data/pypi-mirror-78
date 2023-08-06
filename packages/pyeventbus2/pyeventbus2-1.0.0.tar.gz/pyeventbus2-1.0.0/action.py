from pyeventbus import subscriber


class ObserverAction():

    def __init__(self, target: subscriber.DefaultSubscriber, method: str):
        assert target is not None, f"{target} must be not None"
        # assert issubclass(target, object), f"{target} muse be class"
        # assert callable(method)
        self.__target = target
        self.__method = method

    def do_execute(self, event: object) -> object:  # event是method方法的参数
        try:
            return getattr(self.__target, self.__method)(event)
        except Exception as e:
            print(str(e))

from pyeventbus import subscriber, msg


def msg_type(msg_instance):
    # return f"{msg_class.__module__}.{msg_class.__name__}"
    return type(msg_instance)


OBSERVER_REGISTRY = [
    {
        msg_type(msg.DictMessage()): [
            subscriber.AConcreteObserver()
        ]
    },
    {
        msg_type(msg.IntMessage()): [
            subscriber.BConcreteObserver(),
            subscriber.CConcreteObserver(),

        ]
    },
]

class Message():
    pass


class XMessage(Message):
    pass


class YMessage(Message):
    pass


class IntMessage(int):
    pass
    # def __init__(self, x=1, base=10):
    #     super(IntMessage, self).__init__(x, base=base)


class DictMessage(dict):
    pass

    # def __setattr__(self, key, value):
    #     self.__dict__[key] = value

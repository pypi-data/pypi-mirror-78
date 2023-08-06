# 同时支持的同步和异步消息通知的eventbus，灵感来自与google guava eventbus

用法：
1.定义接收消息类型：
```
class IntMessage(int):
    pass

class DictMessage(dict):
    pass
```
    
2.定义需要接收消息的Observer类，需继承subscriber.DefaultSubscriber，
并实现subscribe方法，subscribe方法的参数类型与自定义的消息类型保持一致
```
class CConcreteObserver(DefaultSubscriber):

    def subscribe(self, msg: msg.IntMessage):
        time.sleep(2)
        print(f"{self.__class__.__name__}#{inspect.stack()[0][3]}: msg:{msg}")
```      
 
3.根据消息类型，添加接收者
```
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
```

4.在需要的地方引入eventbus，根据自己的需求选择支持同步的方式（eventbus.EventBus）或异步的方式（eventbus.AsyncEventBus）
在消息接收处，调用notify接口发送消息给对应的所有观察者
```
sync_event_bus = eventbus.AsyncEventBus()
sync_event_bus.notify(msg.IntMessage(1211))
```
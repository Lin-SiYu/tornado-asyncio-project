# tornado-asyncio-project
a tornado project focus on asyncio

[TOC]

# 一、HeartBeat

- **HeartBeat.count** - 获取心跳次数
- **HeratBeart.ticker** - 启动心跳的执行，默认为1秒执行一次
- **HeratBeart.register** - 注册每次心跳时执行的任务（异步任务），interval 参数作为该函数执行回调的时间间隔
- **HeratBeart.unregister** - 注销指定 task_id 的回调任务
- **HeratBeart.alive** - 使用MQ的生产者，执行即触发MQ的推送

## 1-1 使用方式

```python
from lib.heartbeat import heartbeat

# 任意位置，调用即注册
# 对需要使用心跳回调的函数（异步函数），调用regiaster即可
heartbeat.register(self._check_connection, 60)
```

## 1-2 基本配置

```python
# config.py

# 心跳打印时间间隔(秒)，默认为0为不打印
HEARTBEAT_INTERVAL = 30
# 心跳广播间隔(秒)，默认为0为不广播
HEARTBEAT_BROADCAST = 30
```

# 二、RabbitMQ

- **MqBase**- 基于aioamqp 的基础类，用于操作 mq
  - async def **connect** - 连接 MQ，提供所需 channel，初始化基于 config 的 exchange
  - async def **producer** - 生产者，初始化 exchange 操作
  - async def **publish** - 生产者广播，将 msg 广播至指定的exchange
  - async def **consumer** - 消费者，初始化 queue，绑定指定 exchange
  - async def **subscribe** - 消费者订阅，订阅指定 queue，并回调 函数（必须为异步函数）
  - **！！！注意！！！**类下所有函数，exchange_name、exchange_type、queue_name 相关参数，**切勿使用None作为空传入**
- **MQConsumer** - 给需要订阅操作的消费者，提供注册方法。
  - async def **register** - 将需要订阅的消费者 append 入类内列表，用于后续调用执行
  - **MQConsumer.subscribers** - 查询消费者注册列表（用于订阅对象查询）

## 2-1 基本使用流程

1. **在config.py文件内，添加需要初始化的 exchange**

   ```python
   # config.py
   EXCHANGES_DICT = {
       'fanout': ('Heartbeat',),
       'topic': ('MyTestExchange',),
       'direct': ()
   }
   ```

2. **在app/mq_consumer_register.py文件内，register 函数内，注册消费者**

   ```python
   from lib.rabbit_mq.consumer import consumer
   from lib.rabbit_mq.heartbeat_consumer import heartbeat_example
   
   
   async def register():
       '''
       根据业务逻辑，注册需要初始化队列的对象信息
       ！注意！：需保证exchange存在
       '''
       # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
       # await consumer.register(heartbeat_example, 'heartbeat_test', 'Heartbeat')
       pass
   
   ```

3. **生产者的创建，基于业务逻辑，详情参考2-2**

## 2-3 详细整理

### 2-3-1 mq实例对象调用方式

建议使用在 app 内放置的 mq 对象，MqBase 类为非单例类。

```python
# 若使用位置存在app对象 （执行 Main 类下）
mq = qpp.mq

# 若使用位置不存在app对象（APIHandler 类下）
mq = self.application.mq
```

### 2-3-2 初始化 exchange 

```python
# 将在 MqBase 实例，执行 connect() 内进行初始化操作。
# run.py - Main - initialize()
self.loop.run_sync(self.app.mq.connect)

# config.py
EXCHANGES_DICT = {
    'fanout': ('Heartbeat',),
    'topic': ('MyTestExchange',),
    'direct': ()
}
```

### 2-3-3 生产者的publish方式

#### 方式一、使用 asyncio 、tornado 的 loop

```python
 def alive(self, app):
     mq = app.mq
     exchange_name = 'Heartbeat'
     loop = asyncio.get_event_loop()
     data = {'count': self.count}
     loop.create_task(mq.publish(data, exchange_name, ))
```

```python
 def alive(self, app):
     mq = app.mq
     exchange_name = 'Heartbeat'
     loop = IOLoop.instance()
     data = {'count': self.count}
     loop.add_callback(mq.publish，data, exchange_name, )
```

#### 方式二、async 函数 、 tornado.gen 包裹下

```python
from tornado import gen

@gen.coroutine
def get(self):
    mq = app.mq
    exchange_name = 'test'
    data = "hello,mq"
    # yield mq.producer(exchange_name,'fanout')
    yield mq.publish(data, exchange_name)
    self.write(self.success_json(data))
```

```python
async def get(self):
    mq = app.mq
    exchange_name = 'test'
    data = "hello,mq"
    # await mq.producer(exchange_name,'fanout')
    await mq.publish(data, exchange_name)
    self.write(self.success_json(data))
```

### 2-3-4 消费者的队列初始化、订阅操作

```python
'''/mq_consumer_register.py - register()'''
from tornado_project.common_utilities.rabbit_mq.consumer import consumer
from tornado_project.common_utilities.rabbit_mq.heartbeat_consumer import heartbeat_example


async def register():
    '''
    根据业务逻辑，注册需要初始化队列的对象信息
    ！注意！：需保证exchange存在
    '''
    # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
    # await consumer.register(heartbeat_example, 'heartbeat_test', 'Heartbeat')
    # await consumer.register(MongodbWatchMiddleware().publish, 'mongo_watch', 'Mongodb')
    pass

```

```python
# e.g. 消费者异步回调函数
# 具体参数分析，详见 aioamqp 官方文档
# https://aioamqp.readthedocs.io/en/latest/api.html#publishing-messages
async def heartbeat_example( channel, body, envelope, properties):
    # todo 业务逻辑
    print('hello mytest')
```


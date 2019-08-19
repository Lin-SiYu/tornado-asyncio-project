from tornado_project.common_utilities.rabbit_mq.consumer import consumer
from tornado_project.common_utilities.rabbit_mq.heartbeat_consumer import heartbeat_example


async def register():
    '''
    根据业务逻辑，注册需要初始化队列的对象信息
    ！注意！：需保证exchange存在
    '''
    # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
    await consumer.register(heartbeat_example, 'heartbeat_test', 'Heartbeat')
    # await consumer.register(MongodbWatchMiddleware().publish, 'mongo_watch', 'Mongodb')
    await consumer.register(heartbeat_example, 'mongo.watch', 'Mongodb', routing_key='*.watch')
    await consumer.register(heartbeat_example, 'mongo.watch', 'Mongodb', routing_key='mongo.#')
    # pass

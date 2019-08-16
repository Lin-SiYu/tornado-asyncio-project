from tornado_project.common_utilities.decorators.locker_decorators import async_method_locker
from tornado_project.common_utilities.log import logger_info


class MQConsumer:
    def __init__(self, ):
        self._subscribers = []  # e.g. [{data_dict}, ...]

    @async_method_locker("MQConsumer.register")
    async def register(self, async_callback, queue_name, exchange_name, routing_key='', prefetch_count=1):
        data_dict = dict(
            async_callback=async_callback,
            queue_name=queue_name,
            exchange_name=exchange_name,
            routing_key=routing_key,
            prefetch_count=prefetch_count,
        )
        self._subscribers.append(data_dict)
        logger_info.info('%s - Subscribers append success! queue_name:%s' % (self, queue_name))

    @property
    def subscribers(self):
        return self._subscribers


consumer = MQConsumer()

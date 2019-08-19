import asyncio
import json

import aioamqp
from aioamqp import SynchronizationError
from tornado.options import options

from tornado_project.common_utilities.heartbeat import heartbeat
from tornado_project.common_utilities.log import logger_info, logger_error


class MqBase:
    def __init__(self):
        settings = options.as_dict()
        self._host = settings.get('MQ_HOST', None)
        self._port = settings.get('MQ_PORT', None)
        self._username = settings.get('MQ_USER', None)
        self._pwd = settings.get('MQ_PWD', None)
        self._connected = False  # If connect success.
        self._protocol = None
        self._channel = None  # Connection channel.

        # Register a loop run task to check TCP connection's healthy.
        heartbeat.register(self._check_connection, 60)

    async def connect(self):
        '''
        连接 RabbitMQ,并初始化exchanges
        :param reconnect: 若连接非初连接，进行重置操作
        :return:
        '''
        # 若已连接，则不进行连接操作
        if self._connected:
            return
        logger_info.info('Host:%s,Port:%s - Try connecting RabbitMQ!' % (self._host, self._port))

        try:
            transport, protocol = await aioamqp.connect(host=self._host, port=self._port, login=self._username,
                                                        password=self._pwd)
        except aioamqp.AmqpClosedConnection as  e:
            logger_error.error('Rabbit connection error:%s' % e)
            return
        finally:
            if self._connected:
                return
        self._protocol = protocol
        self._channel = await protocol.channel()
        self._connected = True
        await self._init_exchanges()
        logger_info.info("%s - RabbitMQ initialize success!" % self)

    async def _init_exchanges(self):
        exchanges = options.EXCHANGES_DICT
        try:
            for e_type, e_names in exchanges.items():
                if e_type not in ['fanout', 'topic', 'direct']:
                    raise Exception("GET THE WRONG EXCHANGE TYPE! PLEASE CHECK OUT!")
                for e_name in e_names:
                    await self.producer(e_name, e_type)
        except Exception as e:
            logger_error.error('%s - Exchange init error : %s' % (self, e))

    async def _check_connection(self, task_id, *args, **kwargs):
        if self._connected and self._channel and self._channel.is_open:
            logger_info.info("%s - RabbitMQ connection ok." % self)
            return
        logger_error.error("%s - CONNECTION LOSE! START RECONNECT RIGHT NOW!" % self)
        self._connected = False
        self._protocol = None
        self._channel = None
        self._event_handler = {}
        asyncio.get_event_loop().create_task(self.connect())

    async def producer(self, exchange_name='', exchange_type='', *args, **kwargs):
        '''
        生产者初始化exchange
        :return:
        '''
        await self._channel.exchange_declare(exchange_name=exchange_name, type_name=exchange_type, auto_delete=True,
                                             *args, **kwargs)
        logger_info.info('%s - Create exchange success! name:%s,type:%s' % (self, exchange_name, exchange_type))

    async def publish(self, msg, exchange_name='', routing_key='', *args, **kwargs):
        '''
        广播至指定的exchange
        :param msg: 接受dict，处理成json格式
        :return:
        '''
        if not self._connected:
            logger_error.error("RabbitMQ not ready right now!", caller=self)
            return
        json_msg = json.dumps(msg)
        await self._channel.basic_publish(payload=json_msg, exchange_name=exchange_name, routing_key=routing_key, *args,
                                          **kwargs)
        logger_info.info('%s - Publish messages success! name:%s' % (self, exchange_name))

    async def consumer(self, queue_name='', exchange_name='', routing_key='', prefetch_count=1, *args, **kwargs):
        '''
        e消费者初始化queue，绑定指定exchang
        :return:
        '''
        try:
            await self._channel.queue_declare(queue_name=queue_name, auto_delete=True)
        except SynchronizationError as e:
            pass
        await self._channel.queue_bind(queue_name=queue_name, exchange_name=exchange_name,
                                       routing_key=routing_key)
        await self._channel.basic_qos(prefetch_count=prefetch_count)
        logger_info.info(
            '%s - Consumer initialize success! exchange_name=%s,queue_name:%s' % (self, exchange_name, queue_name))

    async def subscribe(self, async_callback=None, queue_name='', *args, **kwargs):
        '''
        订阅指定队列
         async_callback : must Asynchronous callback.
        :return:
        '''
        await self._channel.basic_consume(async_callback, queue_name=queue_name, no_ack=True)
        logger_info.info('%s - Subscribe success! queue_name:%s' % (self, queue_name))

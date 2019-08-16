# -*- coding:utf-8 -*-

import asyncio

from tornado.options import options

from tornado_project.common_utilities import tools
from tornado_project.common_utilities.log import logger_info

__all__ = ("heartbeat",)


class HeartBeat(object):

    def __init__(self):
        settings = options.as_dict()
        self._count = 0  # 心跳次数
        self._interval = 1  # 服务心跳执行时间间隔(秒)
        self._print_interval = settings.get('HEARTBEAT_INTERVAL', 0)  # 心跳打印时间间隔(秒)，0为不打印
        self._broadcast_interval = settings.get('HEARTBEAT_BROADCAST', 0)  # 心跳广播间隔(秒)，0为不广播
        self._tasks = {}  # 跟随心跳执行的回调任务列表，由 self.register 注册 {task_id: {...}}

    @property
    def count(self):
        return self._count

    def ticker(self, app=None):
        """ 启动心跳， 每秒执行一次
        """
        self._count += 1

        # 打印心跳次数
        if self._print_interval > 0:
            if self._count % self._print_interval == 0:
                logger_info.info("Do server heartbeat, count:%s" % self._count)

        # 设置下一次心跳回调
        asyncio.get_event_loop().call_later(self._interval, self.ticker, app)

        # 执行任务回调
        for task_id, task in self._tasks.items():
            interval = task["interval"]
            if self._count % interval != 0:
                continue
            func = task["func"]
            args = task["args"]
            kwargs = task["kwargs"]
            kwargs["task_id"] = task_id
            kwargs["heart_beat_count"] = self._count
            asyncio.get_event_loop().create_task(func(*args, **kwargs))

        # 广播服务进程心跳
        if self._broadcast_interval > 0:
            if self._count % self._broadcast_interval == 0:
                self.alive(app)

    def register(self, func, interval=1, *args, **kwargs):
        """ 注册一个任务，在每次心跳的时候执行调用
        @param func 心跳的时候执行的函数
        @param interval 执行回调的时间间隔(秒)
        @return task_id 任务id
        """
        t = {
            "func": func,
            "interval": interval,
            "args": args,
            "kwargs": kwargs
        }
        task_id = tools.get_uuid1()
        self._tasks[task_id] = t
        return task_id

    def unregister(self, task_id):
        """ 注销一个任务
        @param task_id 任务id
        """
        if task_id in self._tasks:
            self._tasks.pop(task_id)

    def alive(self, app):
        """ 服务进程广播心跳 - 生产者
        """
        mq = app.mq
        exchange_name = 'Heartbeat'
        loop = asyncio.get_event_loop()
        data = {'count': self.count}
        loop.create_task(mq.publish(data, exchange_name, ))


heartbeat = HeartBeat()

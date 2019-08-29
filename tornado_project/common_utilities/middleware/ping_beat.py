import gzip
import json
import time

from tornado.options import options

from tornado_project.common_utilities.heartbeat import heartbeat
from tornado_project.common_utilities.log import logger_info
from ..middleware import WS_CONNECT_USER_INFOS as user_infos


class BeatPing(object):
    def __init__(self, ping=None, bool_gzip=True):
        '''
        :param ping: 指定发送的ping内容，默认为13位时间戳
        :param bool_gzip: 是否压缩，默认为压缩
        '''
        if not hasattr(user_infos, 'PingMiddleware'):
            user_infos['PingMiddleware'] = {}
        self.user_infos = user_infos['PingMiddleware']
        self.bool_gizp = bool_gzip
        if not ping:
            self.ping = round(time.time() * 1000)
        else:
            self.ping = ping
        self.interval = options.as_dict().get('BEAT_PING_INTERVAL', 0)
        if self.interval:
            heartbeat.register(self.beat_ping, self.interval)

    async def beat_ping(self, *args, **kwargs):
        '''
        向所有用户推送ping dict，若没有 pong 返回则断开连接
        - ping值默认为13位时间戳
        - 推送数据手动 gzip 压缩
        :return: None
        '''
        logger_info.info('Beat-Ping is running.')
        data_dic = {'ping': self.ping}
        if self.bool_gizp:
            data = self.get_gzip(data_dic)
        else:
            data = data_dic
        for user in self.user_infos:
            user.write_message(data, binary=self.bool_gizp)
            self.user_infos[user]['ping'] = data_dic['ping']
            if self.user_infos[user]['count'] == 2:
                user.close()
                self.user_infos.pop(user)
            else:
                self.user_infos[user]['count'] += 1

    def get_gzip(self, ping_data):
        '''
        :param ping_data: {'ping': self.ping}
        :return: gzip data
        '''
        ping_json = json.dumps(ping_data)
        ping_byte = bytes(ping_json, encoding='utf-8')
        ping_gzip = gzip.compress(ping_byte)
        return ping_gzip

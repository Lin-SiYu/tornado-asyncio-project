import gzip

from tornado_project.common_utilities.ws_base import WSMiddleware
from tornado_project.common_utilities.middleware import WEBSOCKET_CLIENT as ws_clients


class ExampleMiddleware(WSMiddleware):
    def process_open(self, ws):
        ws_clients['ExampleMiddleware'][ws] = dict(meaningless=0)
        pass

    def process_message(self, ws):
        # todo 前端发送的数据处理
        pass

    def process_close(self, ws):
        if ws_clients['ExampleMiddleware'].get(ws):
            # 若非自然断开连接，则删除字典内信息
            ws_clients['ExampleMiddleware'].pop(ws)

    async def publish(self, channel, body, envelope, properties):
        # todo 监听 mq 的数据处理,推送连接的用户
        # body 为 bytes 类型
        # 看业务需求是否进行gzip加密，传输二进制数据必须开启binary
        # client端也需要进行gzip解密
        data = gzip.compress(body)
        for user in ws_clients['ExampleMiddleware']:
            user.write_message(data, binary=True)

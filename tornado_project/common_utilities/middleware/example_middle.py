import gzip

from tornado_project.common_utilities.middleware.ws_middle_base import WSMiddleware
from ..middleware import WS_CONNECT_USER_INFOS as user_infos


class ExampleMiddleware(WSMiddleware):
    def process_open(self, ws):
        # ！！注意，下方字典不可为空(若初始为字典)
        user_infos['ExampleMiddleware'][self] = dict(meaningless=0)

    def process_message(self, ws):
        # todo 前端发送的数据处理
        pass

    def process_close(self, ws):
        if user_infos['ExampleMiddleware'].get(self):
            # 若非自然断开连接，则删除字典内信息
            user_infos['ExampleMiddleware'].pop(self)

    async def publish(self, channel, body, envelope, properties):
        # todo 监听 mq 的数据处理,推送连接的用户
        # body 为 bytes 类型
        # 看业务需求是否进行gzip加密，传输二进制数据必须开启binary
        # client端也需要进行gzip解密
        data = gzip.compress(body)
        for user in user_infos['ExampleMiddleware']:
            user.write_message(data, binary=True)

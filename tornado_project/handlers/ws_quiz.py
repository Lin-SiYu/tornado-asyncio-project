import json

from tornado_project.common_utilities.ws_base import WSHandler


class QuizHandler(WSHandler):
    def open_handle(self):
        if 'conn_client' not in self.handler_info:
            self.handler_info['conn_client'] = {}
        sec_key = self.request.headers.get('Sec-Websocket-Key')
        self.handler_info['conn_client'][sec_key] = self

    async def msg_handle(self, message):
        message = json.loads(message)
        print(message)
        # conn = self.settings['redis'].get_conn()
        # if message['operate'] == 'match':
        #     # get_val = await conn.get('matching_users')
        #     if not await conn.exists('matching_users'):
        #         # user_info = dict(user=message['user_id'], user_ws=pickle.dumps(self))
        #         # print(user_info)
        #         # info_pik = pickle.dumps(user_info)
        #         # await conn.lpush('matching_users', info_pik)
        #         print(self.application)
        if message['operate'] == 'match':
            if 'matching_users' in self.handler_info:
                matching_users = self.handler_info['matching_users']
                matching_users[message['user_id']] = self
            else:
                self.set_handler_info('matching_users', {message['user_id']: self})
            print(self.handler_info)
        pass

    def close_handle(self):
        sec_key = self.request.headers.get('Sec-Websocket-Key')
        self.handler_info['conn_client'].pop(sec_key)

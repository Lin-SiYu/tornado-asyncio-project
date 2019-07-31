from tornado_project.handlers import APIHandler


class RedisAPIHandler(APIHandler):
    async def get(self):
        conn = self.settings['redis'].get_conn()
        val = await conn.set('xxx', 123)
        # get_val = await conn..get('xxx')
        self.write(self.success_json('ok', '200', val))

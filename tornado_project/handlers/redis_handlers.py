from tornado_project.handlers import APIHandler


class RedisAPIHandler(APIHandler):
    async def get(self):
        val = await self.settings['redis'].set('xxx', 123)
        # get_val = await self.settings['redis'].get()
        self.write(self.success_json('ok', '200', val))

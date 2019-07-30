from tornado_project.common_utilities.sql.peewee_models.test_model import Test
from tornado_project.handlers import APIHandler


class SqlHandler(APIHandler):
    async def get(self):
        sql_manager = self.settings['sql'].get_manager()
        all_objects = await sql_manager.execute(Test.select())
        for obj in all_objects:
            self.write(self.success_json('ok', '200', obj.name))

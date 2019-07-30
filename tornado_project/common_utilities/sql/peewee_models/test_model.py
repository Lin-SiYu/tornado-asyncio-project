import peewee

from tornado_project.common_utilities.sql.peewee_models.base_model import BaseModel


# 类名必须和表名对应
class Test(BaseModel):
    name = peewee.CharField()

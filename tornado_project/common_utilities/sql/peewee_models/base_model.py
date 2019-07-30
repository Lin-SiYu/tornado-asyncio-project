import peewee

from tornado_project.common_utilities.sql.sql_base import MySQLHandler


class BaseModel(peewee.Model):
    class Meta:
        database = MySQLHandler().get_conn()

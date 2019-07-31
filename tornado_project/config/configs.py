COOKIE_SECRET = 'THIS_IS_COOKIE_SECRET'
PORT = 8080
DEBUG = False

SHUTDOWN_MAX_WAIT_TIME = 1 * 1
INFO_LOG_PATH = "../tornado_project/logs/info.log"
DEBUG_LOG_PATH = "../tornado_project/logs/debug.log"
ERROR_LOG_PATH = "../tornado_project/logs/error.log"
ACC_LOG_PATH = "../tornado_project/logs/access.log"
LOG_BACKUP = 7
LOG_ROTATE_DAY = 7

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'test'

SQL_HOST = 'localhost'
SQL_POST = 3306
SQL_USER = 'test'
SQL_PWD = 'test123'
SQL_MAX_CONN = 10
SQL_DB_NAME = 'test'

REDIS_URL = 'redis://localhost/'
REDIS_DB = 10
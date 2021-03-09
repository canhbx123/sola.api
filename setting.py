import os

from flask_caching import Cache
from common.dmysql import Dmysql
from common.config import MYSQL_CONFIG
from pathlib import Path
from datetime import timedelta
import redis

cache = Cache(config={'CACHE_TYPE': 'redis'})


def get_smy():
    return Dmysql(host=MYSQL_CONFIG['host'], port=MYSQL_CONFIG['port'], user=MYSQL_CONFIG['user'], passwd=MYSQL_CONFIG['passwd'], db=MYSQL_CONFIG['db'])


SMY = get_smy

ROLES = {
    'ADMIN': 1,
    'MASTER': 2,
    'MANAGER': 3,
    'LEADER': 4,
    'WORKER': 5,
    'ACCOUNTANT': 6
}
DEFAULT_PASSWORD = 'abcd@sola'

SESSION_ID_NAME = 'sid'
SESSION_EXPIRE = timedelta(days=365)

ID2ROLES = {v: k for k, v in ROLES.items()}

DNN_PATH = Path('/home/dnn/sola')
EXPENSE_PATH = DNN_PATH / 'expense'
COMPANY_ATTACHMENT_PATH = DNN_PATH / 'company/attachment'
if not os.path.isdir(COMPANY_ATTACHMENT_PATH):
    os.makedirs(COMPANY_ATTACHMENT_PATH)

if not os.path.isdir(EXPENSE_PATH):
    os.makedirs(EXPENSE_PATH)


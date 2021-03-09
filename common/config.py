import os

if os.environ.get('PRODUCTION'):
    WEB_CONFIG = {
        'CACHE_REDIS_HOST': '127.0.0.1',
        'PERMANENT_SESSION_LIFETIME': 86400,
        'JSONIFY_PRETTYPRINT_REGULAR': False,
        'JSON_SORT_KEYS': False,
        'MAX_CONTENT_LENGTH': 100 * 1024 * 1024,
        'SECRET_KEY': 'BSRE^^^(@!!@JJDDKKFNND',
        'RUN_DOMAIN': 'http://solajapan.xyz'

    }
    MYSQL_CONFIG = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'Slp422word!@#',
        'db': 'sola'
    }
else:
    WEB_CONFIG = {
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_KEY_PREFIX': 'localhost',
        'JSONIFY_PRETTYPRINT_REGULAR': False,
        'JSON_SORT_KEYS': False,
        'MAX_CONTENT_LENGTH': 100 * 1024 * 1024,
        'SECRET_KEY': 'BSRE^^^(@!!@JJDDKKFNND',
        'RUN_DOMAIN': 'http://127.0.0.1:5000'

    }
    MYSQL_CONFIG = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'sola'
    }

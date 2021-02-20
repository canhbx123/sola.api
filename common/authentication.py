from functools import wraps
from common.config import WEB_CONFIG
import hashlib
import uuid
from setting import SESSION_ID_NAME, cache, SESSION_EXPIRE
from flask import request
from setting import SESSION_ID_NAME
import inspect


def get_session_id():
    return request.headers.get(SESSION_ID_NAME)


class Authenticaton:
    @staticmethod
    def set(data):
        session_id = str(uuid.uuid4())
        cache.set(session_id, data, SESSION_EXPIRE)
        return session_id

    @staticmethod
    def get():
        session_id = get_session_id()
        if not session_id:
            return
        return cache.get(session_id)

    @staticmethod
    def clear():
        session_id = get_session_id()
        if not session_id:
            return
        return cache.delete(session_id)


def login_required_json(roles: list = None):
    def __dct(func):
        @wraps(func)
        def __fdecorated(*args, **kwargs):
            log = Authenticaton.get()
            if log and log['id'] > 0:
                if roles and not {log['role']} & set(roles):
                    return {'err': 1}
                log_kw = inspect.signature(func).parameters.get('log')
                if log_kw:
                    kwargs['log'] = log
                return func(*args, **kwargs)
            return {'err': 1}

        return __fdecorated

    return __dct


def generate_hash_password(pwd):
    salt = pwd + WEB_CONFIG['SECRET_KEY']
    return hashlib.md5(salt.encode('utf-8')).hexdigest()


def api_secret(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # _ = request.headers.get('bs') or request.args.get('_')
        # if not _:
        #     return abort(403)
        # rs = _.split('.')
        # if len(rs) != 2:
        #     return abort(403)
        # tk, dtime = rs
        # tk = int(tk)
        # difftime = int(dtime) - int(time.time() * 1000)
        # if abs(difftime) > 30000 or gsecret.gen_key(dtime) != tk:
        #     return abort(403)
        return f(*args, **kwargs)

    return decorated_function

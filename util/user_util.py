from setting import SMY
from common.authentication import generate_hash_password


class UserUtil:
    def login(self):
        pass

    @staticmethod
    # @cache.memoize(timeout=60 * 5)
    def get_logged_info(user_id):
        return SMY().query_row('SELECT *,(SELECT slug FROM EM_role WHERE id=EM_user.role_id) AS role  FROM EM_user WHERE id=:id AND locked=0', {'id': user_id})

    @staticmethod
    def get_login_from_username_password(username, password):
        password_hash = generate_hash_password(password)
        return SMY().query_row('SELECT id,role_id, (SELECT slug FROM EM_role WHERE id=EM_user.role_id) AS role   FROM EM_user WHERE username=:username AND password=:password AND locked=0',
                               {'username': username, 'password': password_hash})

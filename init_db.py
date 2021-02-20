from datetime import datetime

from setting import ROLES, SMY
from common.authentication import generate_hash_password
import sys


class InitDb:
    DEFAULT_PASSWORD = '112233@ok'
    def check_exist_admin(self):
        return SMY().query_row('SELECT id FROM EM_user WHERE  role_id=:role_id', {'role_id': ROLES['ADMIN']})

    def create_admin(self):
        if not self.check_exist_admin():
            user = {
                'username': 'admin',
                'fullname': "Administrator",
                'locked': 0,
                'gender': 1,
                'birthday': '1990-11-14',
                'password': generate_hash_password(self.DEFAULT_PASSWORD),
                'role_id': ROLES['ADMIN'],
                'department_id': 1
            }
            SMY().insert('EM_user', user)


if __name__ == '__main__':
    if sys.argv[1] == 'create_admin':
        InitDb().create_admin()

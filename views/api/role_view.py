from flask_classful import FlaskView, route
from common import decorators
from common.authentication import login_required_json, api_secret
from setting import SMY
from itertools import dropwhile


class RoleView(FlaskView):
    ROLES = SMY().query_table('SELECT * FROM EM_role ORDER BY priority ASC;')
    ROLES_DICT = {role['id']: role for role in ROLES}

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self, log=None):
        role_priority = self.ROLES_DICT[log['role_id']]['priority']
        return {'err': 0, 'data': [role for role in self.ROLES if role_priority == 1 or role['priority'] >= role_priority]}

from flask_classful import FlaskView, route
from common import decorators
from common.authentication import login_required_json, api_secret
from setting import SMY


class RoleView(FlaskView):

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self):
        return SMY().query_table('SELECT * FROM EM_role')

from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request

from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY


class NotificationView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def list(self):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        params = {}
        filters = grid.get('filters')
        _search = filters.get('filter')
        if _search:
            criterias.append('AND content LIKE :querylk1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_notification', criterias=criterias, params=params).render()

    @route('/recent', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def recent(self):
        result = SMY().query_table('SELECT * FROM EM_notification WHERE locked=0 ORDER BY created_time DESC LIMIT 10;')
        return {'err': 0, 'data': result}

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def insert(self, log=None):
        content = request.json.get('content')
        data = {
            'content': content,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
            'created_time': datetime.now(),
            'created_user': log['id']
        }
        rs = SMY().insert(table='EM_notification', data=data)
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def remove(self, log=None):
        department_id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_notification', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        content = request.json.get('content')
        department_id = request.json.get('id')
        data = {
            'content': content,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_notification', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def restore(self, log=None):
        department_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_notification', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

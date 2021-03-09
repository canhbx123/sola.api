from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request

from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY


class JobTitleView(FlaskView):

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
            criterias.append('AND name LIKE :querylk1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_jobtitle', criterias=criterias, params=params).render()

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self, log=None):
        return SMY().query_table('SELECT * FROM EM_jobtitle WHERE locked=0 ORDER BY priority ASC;')

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def insert(self):
        name = request.json.get('name')
        priority = request.json.get('priority')
        description = request.json.get('description')
        data = {
            'name': name,
            'locked': 0,
            'priority': priority,
            'description': description,
            'modified': datetime.now()
        }
        rs = SMY().insert(table='EM_jobtitle', data=data)
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def remove(self):
        object_id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_jobtitle', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self,log=None):
        name = request.json.get('name')
        priority = request.json.get('priority')

        description = request.json.get('description')
        department_id = request.json.get('id')
        data = {
            'name': name,
            'priority': priority,
            'description': description,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_jobtitle', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def restore(self):
        department_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_jobtitle', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

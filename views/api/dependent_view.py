from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request

from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY


class DependentView(FlaskView):

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
        if filters.get('is_dependent'):
            criterias.append('AND is_dependent=1')
        return SqlGrid(conn=SMY(), query='SELECT D.*,(SELECT name FROM EM_relationship WHERE id=D.relationship_id) as relationship', fromdb='FROM EM_dependent D', criterias=criterias,
                       params=params).render()

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def insert(self, log=None):
        name = request.json.get('name')
        furigana = request.json.get('furigana')
        is_dependent = request.json.get('is_dependent')
        relationship_id = request.json.get('relationship_id')
        birthday = request.json.get('birthday')
        employee_id = request.json.get('employee_id')
        data = {
            'name': name,
            'furigana': furigana,
            'employee_id': employee_id,
            'relationship_id': relationship_id,
            'birthday': birthday,
            'is_dependent': is_dependent,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
            'created_time': datetime.now(),
            'created_user': log['id']
        }
        rs = SMY().insert(table='EM_dependent', data=data)
        if rs:
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
        rs = SMY().update(table='EM_dependent', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        name = request.json.get('name')
        furigana = request.json.get('furigana')
        is_dependent = request.json.get('is_dependent')
        relationship_id = request.json.get('relationship_id')
        birthday = request.json.get('birthday')
        employee_id = request.json.get('employee_id')
        object_id = request.json.get('id')
        data = {
            'name': name,
            'furigana': furigana,
            'employee_id': employee_id,
            'relationship_id': relationship_id,
            'birthday': birthday,
            'is_dependent': is_dependent,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_dependent', data=data, where={'id': object_id})
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
        rs = SMY().update(table='EM_dependent', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

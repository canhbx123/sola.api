from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request

from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY


class RelationshipView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def list(self):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_relationship', criterias=criterias).render()

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self):
        return SMY().query_table('SELECT * FROM EM_relationship WHERE locked=0')

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self):
        name = request.json.get('name')
        priority = request.json.get('priority')
        data = {
            'name': name,
            'locked': 0,
            'priority': priority
        }
        rs = SMY().insert(table='EM_relationship', data=data)
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        name = request.json.get('name')
        priority = request.json.get('priority')
        department_id = request.json.get('id')
        data = {
            'name': name,
            'priority': priority,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_relationship', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def remove(self):
        department_id = request.json.get('id')
        data = {
            'locked': 1
        }
        rs = SMY().update(table='EM_relationship', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def restore(self):
        id = request.json.get('id')
        data = {
            'locked': 0,
        }
        rs = SMY().update(table='EM_relationship', data=data, where={'id': id})
        if rs:
            return {'err': 0}
        return {'err': 1}

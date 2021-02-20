import json
import time
from datetime import datetime

import bson
from bcore.bdatetime import Bdatetime
from flask_classful import FlaskView, route
import ujson
from common import decorators
from common.authentication import login_required_json
from flask import  request

from common.sql_table import SqlGrid
from util.user_util import UserUtil
from common.authentication import login_required_json, api_secret
from setting import SMY


class JobView(FlaskView):

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
            criterias.append('AND username LIKE :querylk1 OR fullname=:query1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_job', criterias=criterias, params=params).render()


    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    # @api_secret
    def insert(self):
        name = request.json.get('name')
        description = request.json.get('description')
        data = {
            'name': name,
            'locked': 0,
            'description': description,
            'modified': datetime.now()
        }
        rs = SMY().insert(table='EM_job', data=data)
        if rs:
            return {'err': 0}
        return {'err': 1}



    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self):
        name = request.json.get('name')
        description = request.json.get('description')
        department_id = request.json.get('id')
        data = {
            'name': name,
            'description': description,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_department', data=data, where={'id': department_id})
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
            'locked': 1,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_department', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self):
        department_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_department', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

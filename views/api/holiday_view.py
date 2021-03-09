import json
import time
from datetime import datetime

import bson
from bcore.bdatetime import Bdatetime
from flask_classful import FlaskView, route
import ujson
from common import decorators
from common.authentication import login_required_json
from flask import request

from common.sql_table import SqlGrid
from util.user_util import UserUtil
from common.authentication import login_required_json, api_secret
from setting import SMY


class HolidayView(FlaskView):
    def __custom_row(self, item):
        item['date'] = item['date'].strftime('%Y-%m-%d')

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
            criterias.append('AND H.reason LIKE :querylk1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND H.locked=0')
        elif tab == 'lock':
            criterias.append('AND H.locked=1')
        elif tab == 'wait':
            criterias.append('AND H.locked=0 AND H.approved=0')
        elif tab == 'approved':
            criterias.append('AND H.locked=0 AND H.approved=1')
        elif tab == 'refuse':
            criterias.append('AND H.locked=0 AND H.approved=-1')
        if filters.get('user_id'):
            criterias.append('AND H.user_id=:user_id')
            params['user_id'] = filters['user_id']
        return SqlGrid(conn=SMY(), query='SELECT H.*, (SELECT fullname FROM EM_user WHERE id=H.user_id) AS user', fromdb='FROM EM_holiday H', criterias=criterias, params=params,
                       custom_row=self.__custom_row).render()

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        user_id = request.json.get('user_id')
        reason = request.json.get('reason')
        date = request.json.get('date')
        data = {
            'user_id': user_id,
            'reason': reason,
            'date': date,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
            'created_user': log['id'],
            'created_time': datetime.now(),
            'approved': 0
        }
        rs = SMY().insert(table='EM_holiday', data=data)
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        reason = request.json.get('reason')
        object_id = request.json.get('id')
        data = {
            'reason': reason,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_holiday', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def remove(self, log=None):
        object_id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_holiday', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self, log=None):
        object_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_holiday', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/action', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self, log=None):
        type = request.json.get('type')
        id = request.json.get('id')
        approved = 1 if type == 'approved' else -1
        data = {
            'approved': approved,
            'approval_user': log['id'],
            'approval_time': datetime.now(),
        }
        rs = SMY().update(table='EM_holiday', data=data, where={'id': id})
        if rs:
            return {'err': 0}
        return {'err': 1}

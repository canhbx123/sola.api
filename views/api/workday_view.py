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


class WorkDayView(FlaskView):

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
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        if filters.get('year'):
            criterias.append('AND year=:year')
            params['year'] = filters['year']
        if filters.get('month'):
            criterias.append('AND month=:month')
            params['month'] = filters['month']
        custom_sort = 'ORDER BY year DESC, month DESC, modified DESC'
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_workdays', criterias=criterias, params=params, custom_sort=custom_sort).render()

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        month = request.json.get('month')
        year = request.json.get('year')
        workdays = request.json.get('workdays')
        weekend_days = request.json.get('weekend_days')
        national_holiday = request.json.get('national_holiday')
        now = datetime.now()
        data = {
            'month': month,
            'year': year,
            'workdays': workdays,
            'weekend_days': weekend_days,
            'national_holiday': national_holiday,
            'modified': now,
            'user_modified': log['id'],
            'created_user': log['id'],
            'created_time': now
        }
        rs = SMY().insert(table='EM_workdays', data=data)
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        object_id = request.json.get('id')
        month = request.json.get('month')
        year = request.json.get('year')
        workdays = request.json.get('workdays')
        weekend_days = request.json.get('weekend_days')
        national_holiday = request.json.get('national_holiday')
        now = datetime.now()
        data = {
            'month': month,
            'year': year,
            'workdays': workdays,
            'weekend_days': weekend_days,
            'national_holiday': national_holiday,
            'modified': now,
            'user_modified': log['id'],
        }
        print(data)
        rs = SMY().update(table='EM_workdays', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def remove(self, log=None):
        department_id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_workdays', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self, log=None):
        department_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_workdays', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

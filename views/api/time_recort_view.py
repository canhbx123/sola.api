import mimetypes
from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY, MEMO_PATH
from uuid import uuid4


class TimeRecordView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def list(self):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        filters = grid.get('filters')
        params = {}
        _search = filters.get('filter')
        if _search:
            criterias.append('AND name LIKE :querylk1 OR furigana=:query1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND locked=0')
        elif tab == 'lock':
            criterias.append('AND locked=1')
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_company', criterias=criterias, params=params).render()

    def __check_record(self):
        SMY().query_row('SELECT * FROM EM_time_record WHERE created_time <= :starttime AND  created_time')

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        data = request.json
        data['locked'] = 0
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['user_id'] = log['id']
        company = SMY().query_row('SELECT coords FROM EM_company WHERE locked=0')
        if company:
            rs = SMY().insert(table='EM_company', data=data)
            if rs > 0:
                return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @login_required_json(roles=['admin'])
    @decorators.return_json
    @api_secret
    def update(self, log=None):
        data = dict(request.json)
        if data.get('date_of_establishment'):
            data['date_of_establishment'] = datetime.strptime(data['date_of_establishment'], '%Y/%m/%d')
        else:
            del data['date_of_establishment']
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['created_user'] = log['id']
        _id = data['id']
        rs = SMY().update(table='EM_company', data=data, where={'id': _id})
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

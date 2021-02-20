import mimetypes
from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY, MEMO_PATH
from uuid import uuid4


class CompanyView(FlaskView):

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

    @decorators.return_json
    @login_required_json(roles=['admin'])
    @route('/memo-upload', methods=['POST'])
    def upload(self):
        file = request.files['image']
        company_id = request.form.get('company_id', type=int)
        field = request.form.get('field')
        ext = mimetypes.guess_extension(file.mimetype)
        filename = '%s%s' % (str(uuid4()), ext)
        write_path = MEMO_PATH / filename
        SMY().update('EM_company', data={field: filename}, where={'id': company_id})
        file.save(str(write_path))
        return {
            'src': filename
        }

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        data = dict(request.json)
        if data.get('date_of_establishment'):
            data['date_of_establishment'] = datetime.strptime(data['date_of_establishment'], '%Y/%m/%d')
        else:
            del data['date_of_establishment']
        data['locked'] = 0
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['created_user'] = log['id']
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

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def remove(self):
        _id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_company', data=data, where={'id': _id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self):
        _id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_company', data=data, where={'id': _id})
        if rs:
            return {'err': 0}
        return {'err': 1}

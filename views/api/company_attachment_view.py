import mimetypes
from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY, COMPANY_ATTACHMENT_PATH
from uuid import uuid4


class CompanyAttachmentView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def attachment_list(self):
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
        return SqlGrid(conn=SMY(), query='SELECT *', fromdb='FROM EM_company_attachment', criterias=criterias, params=params).render()

    @decorators.return_json
    @login_required_json(roles=['admin'])
    @route('/upload', methods=['POST'])
    def upload(self, log=None):
        file = request.files['file']
        priority = request.form.get('priority', type=int)
        ext = mimetypes.guess_extension(file.mimetype)
        filename = '%s%s' % (str(uuid4()), ext)
        write_path = COMPANY_ATTACHMENT_PATH / filename
        file.save(str(write_path))
        now = datetime.now()
        data = {
            'name': request.form.get('file_name'),
            'path': filename,
            'priority': priority,
            'locked': 0,
            'user_modified': log['id'],
            'created_user': log['id'],
            'modified': now,
            'created_time': now,
        }
        rs = SMY().insert(table='EM_company_attachment', data=data)
        if rs > 0:
            return {'err': 0, 'data': data}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @login_required_json(roles=['admin'])
    @decorators.return_json
    @api_secret
    def update(self, log=None):
        data = dict(request.json)
        data_update = {
            'modified': datetime.now(),
            'user_modified': log['id'],
            'name': data.get('name', ''),
            'priority': data.get('priority', 99)
        }
        _id = data['id']
        rs = SMY().update(table='EM_company_attachment', data=data_update, where={'id': _id})
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def remove(self, log=None):
        _id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_company_attachment', data=data, where={'id': _id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    def restore(self, log=None):
        _id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_company_attachment', data=data, where={'id': _id})
        if rs:
            return {'err': 0}
        return {'err': 1}

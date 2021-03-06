import mimetypes
from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY, COMPANY_ATTACHMENT_PATH
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
    @route('/attachment/upload', methods=['POST'])
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

    def __build_object(self):
        pass

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        name = request.json.get('name')
        furigana = request.json.get('furigana')
        zip = request.json.get('zip')
        address = request.json.get('address')
        date_of_establishment = request.json.get('date_of_establishment')
        number_o_employees = request.json.get('number_o_employees')
        legal_entity_number = request.json.get('legal_entity_number')
        phone_number = request.json.get('phone_number')
        fax_number = request.json.get('fax_number')
        coords = request.json.get('coords')
        if date_of_establishment:
            date_of_establishment = datetime.strptime(date_of_establishment, '%Y/%m/%d')
        data = {
            'name': name,
            'furigana': furigana,
            'zip': zip,
            'address': address,
            'date_of_establishment': date_of_establishment,
            'number_o_employees': number_o_employees,
            'legal_entity_number': legal_entity_number,
            'phone_number': phone_number,
            'fax_number': fax_number,
            'coords': coords,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
            'created_time': datetime.now(),
            'created_user': log['id']
        }
        rs = SMY().insert(table='EM_company', data=data)
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @login_required_json(roles=['admin'])
    @decorators.return_json
    @api_secret
    def update(self, log=None):
        name = request.json.get('name')
        furigana = request.json.get('furigana')
        zip = request.json.get('zip')
        address = request.json.get('address')
        date_of_establishment = request.json.get('date_of_establishment')
        number_o_employees = request.json.get('number_o_employees')
        legal_entity_number = request.json.get('legal_entity_number')
        phone_number = request.json.get('phone_number')
        fax_number = request.json.get('fax_number')
        coords = request.json.get('coords')
        if date_of_establishment:
            date_of_establishment = datetime.strptime(date_of_establishment, '%Y/%m/%d')
        data = {
            'name': name,
            'furigana': furigana,
            'zip': zip,
            'address': address,
            'date_of_establishment': date_of_establishment,
            'number_o_employees': number_o_employees,
            'legal_entity_number': legal_entity_number,
            'phone_number': phone_number,
            'fax_number': fax_number,
            'coords': coords,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
        }
        rs = SMY().update(table='EM_company', data=data, where={'id': request.json.get('id')})
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

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self):
        return SMY().query_table('SELECT * FROM EM_company WHERE locked=0')

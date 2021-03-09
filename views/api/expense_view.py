from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
import uuid
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY, EXPENSE_PATH


class ExpenseView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def list(self):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        params = {}
        filters = grid.get('filters')
        _search = filters.get('filter')
        if tab == 'index':
            criterias.append('AND EM.locked=0')
        elif tab == 'lock':
            criterias.append('AND EM.locked=1')
        if filters.get('employee_id'):
            criterias.append('AND EM.employee_id=:employee_id')
            params['employee_id'] = filters['employee_id']
        if filters.get('from_date'):
            criterias.append('AND EM.created_time > :from_date')
            params['from_date'] = datetime.strptime(filters['from_date'], '%Y-%m-%d')
        if filters.get('to_date'):
            criterias.append('AND EM.created_time < :to_date')
            params['to_date'] = datetime.strptime(filters['to_date'], '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        return SqlGrid(conn=SMY(), query='SELECT EM.*, (SELECT fullname FROM EM_user WHERE id=EM.employee_id) AS user', fromdb='FROM EM_expense_document EM', criterias=criterias,
                       params=params).render()

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self, log=None):
        return SMY().query_table('SELECT * FROM EM_expense_document WHERE locked=0')

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def insert(self, log=None):
        file = request.files.get('file')
        content = request.form.get('content')
        user_id = request.form.get('user_id')
        filename = '%s-%s' % (uuid.uuid4(), file.filename)
        file_write = EXPENSE_PATH / filename
        file.save(file_write)
        data = {
            'employee_id': user_id,
            'content': content,
            'path': filename,
            'locked': 0,
            'modified': datetime.now(),
            'user_modified': log['id'],
            'created_time': datetime.now(),
            'created_user': log['id']
        }
        rs = SMY().insert(table='EM_expense_document', data=data)
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/remove', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def remove(self, log=None):
        object_id = request.json.get('id')
        data = {
            'locked': 1,
            'modified': datetime.now(),
            'user_modified': log['id']
        }
        rs = SMY().update(table='EM_expense_document', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def restore(self):
        object_id = request.json.get('id')
        data = {
            'locked': 0,
            'modified': datetime.now()
        }
        rs = SMY().update(table='EM_expense_document', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

from datetime import datetime
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.authentication import generate_hash_password, Authenticaton
from common.sql_table import SqlGrid
from util.user_util import UserUtil
from common.authentication import login_required_json, api_secret
from setting import SMY, SESSION_ID_NAME, DEFAULT_PASSWORD
import json
from functools import lru_cache
import copy


class UserView(FlaskView):
    menu_config = json.load(open('resource/menu.json'))

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin', 'master', 'leader'])
    @api_secret
    def list(self, log=None):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        filters = grid.get('filters')
        params = {}
        _search = filters.get('filter')
        if _search:
            criterias.append('AND username LIKE :querylk1 OR fullname=:query1')
            params['query1'] = _search
            params['querylk1'] = '%' + params['query1'] + '%'
        if tab == 'index':
            criterias.append('AND U.locked=0')
        elif tab == 'lock':
            criterias.append('AND U.locked=1')
        if filters.get('role_id'):
            criterias.append('AND U.role_id=:role_id')
            params['role_id'] = filters['role_id']
        if filters.get('department_id'):
            criterias.append('AND U.department_id=:department_id')
            params['department_id'] = filters['department_id']
        if filters.get('commute_allowance', 0):
            criterias.append('AND U.commute_allowance=:commute_allowance')
            params['commute_allowance'] = filters['commute_allowance']
        return SqlGrid(conn=SMY(),
                       query='SELECT U.id, U.username, U.fullname, U.gender,U.role_id,U.furigana, U.birthday,U.zip,U.address,U.phone, U.email, U.bank_name, U.branch_name, U.account_type, U.account_number, U.my_number,U.pension_number,U.registration_date,U.insurance_insured_person,U.activeor_retirement_status,U.department_id,U.base_salary,U.commute_allowance,U.modified, U.user_modified,U.created_user,U.created_time,   (SELECT name FROM EM_role WHERE id=U.role_id) AS role,(SELECT name FROM EM_department WHERE id=U.department_id) AS department ',
                       fromdb='FROM EM_user U',
                       criterias=criterias, params=params).render()

    @route('/insert', methods=['POST'])
    @login_required_json(roles=['admin'])
    @decorators.return_json
    @api_secret
    def insert(self, log=None):
        data = dict(request.json)
        if data.get('birthday'):
            data['birthday'] = datetime.strptime(data['birthday'], '%Y/%m/%d')
        else:
            del data['birthday']
        if data.get('registration_date'):
            data['registration_date'] = datetime.strptime(data['registration_date'], '%Y/%m/%d')
        else:
            del data['registration_date']
        data['password'] = generate_hash_password(data['password'])
        data['locked'] = 0
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['created_user'] = log['id']
        rs = SMY().insert(table='EM_user', data=data)
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def update(self, log=None):
        data = dict(request.json)
        if data.get('birthday'):
            data['birthday'] = datetime.strptime(data['birthday'], '%Y/%m/%d')
        else:
            del data['birthday']
        if data.get('registration_date'):
            data['registration_date'] = datetime.strptime(data['registration_date'], '%Y/%m/%d')
        else:
            del data['registration_date']
        if data.get('password'):
            del data['password']
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['created_user'] = log['id']
        _id = data['id']
        del data['id']
        del data['role']
        del data['department']
        rs = SMY().update(table='EM_user', data=data, where={'id': _id})
        if rs > 0:
            return {'err': 0}
        return {'err': 1}

    @route('/logged-info', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    # @api_secret
    def logged_info(self, log=None):
        user_id = log['id']
        result = UserUtil.get_logged_info(user_id=user_id)
        if result:
            del result['password']
            return {'err': 0, 'data': result, 'server_time': datetime.now()}

    @route('/logout', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    # @api_secret
    def logout(self):
        Authenticaton.clear()
        return {'err': 0}

    @route('/change-passwd', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def change_passwd(self, log=None):
        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user_id = log['id']
        if not SMY().query_scalar('SELECT id FROM EM_user WHERE id=:id AND password=:password_hash', {'id': user_id, 'password_hash': generate_hash_password(current_password)}):
            return {'err': 1}
        SMY().update('EM_user', data={'password': generate_hash_password(new_password)}, where={'id': user_id})
        return {'err': 0}

    @route('/reset-password', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def reset_password(self):
        data = request.json
        user_id = data.get('user_id')
        SMY().update('EM_user', data={'password': generate_hash_password(DEFAULT_PASSWORD)}, where={'id': user_id})
        return {'err': 0}

    @route('/login', methods=['POST'])
    @decorators.return_json
    @api_secret
    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return {'err': 1, 'msg': 'Tài khoản hoặc mật khẩu không chính xác!'}
        user = UserUtil.get_login_from_username_password(username=username, password=password)
        if not user:
            return {'err': 1, 'msg': 'Tài khoản hoặc mật khẩu không chính xác!'}
        # session['user_id'] = user['id']
        # session_id = se
        session_id = Authenticaton.set(data=user)
        return {'err': 0, 'data': {SESSION_ID_NAME: session_id}}

    @lru_cache(maxsize=100)
    def __process_menu(self, role):
        menus = copy.deepcopy(self.menu_config)
        menu = [m for m in menus if role in m['roles']]
        for m1 in menu:
            if m1.get('subs'):
                m1['subs'] = [m for m in m1['subs'] if role in m['roles']]
        return menu

    @route('/menu', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def menu(self, log=None):
        role = log['role']
        return self.__process_menu(role=role)

    @route('/count', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def count(self):
        total = SMY().query_scalar('SELECT COUNT(1) FROM EM_user WHERE locked=0')
        return {'err': 0, "data": total}

    @route('/all', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def all(self):
        result = SMY().query_table('SELECT id, fullname, role_id FROM EM_user WHERE locked=0')
        return {'err': 0, "data": result}

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
        rs = SMY().update(table='EM_user', data=data, where={'id': department_id})
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
        rs = SMY().update(table='EM_user', data=data, where={'id': department_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

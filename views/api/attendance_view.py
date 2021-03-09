import mimetypes
from datetime import datetime, timedelta
from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY
from common.distance_util import DistanceUtil


class AttendanceView(FlaskView):

    @route('/list', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin', 'master', 'manager', 'leader', 'accountant'])
    @api_secret
    def list(self):
        grid = request.json
        tab = grid.get('tab')
        criterias = []
        filters = grid.get('filters')
        params = {}
        _search = filters.get('filter')
        if tab == 'index':
            criterias.append('AND RC.locked=0')
        elif tab == 'lock':
            criterias.append('AND RC.locked=1')
        elif tab == 'approved':
            criterias.append('AND approved=1')
        elif tab == 'refuse':
            criterias.append('AND approved=-1')
        if filters.get('user_id'):
            criterias.append('AND user_id=:user_id')
            params['user_id'] = filters['user_id']
        return SqlGrid(conn=SMY(), query='SELECT RC.*, (SELECT fullname FROM EM_user WHERE id=RC.user_id) AS user', fromdb='FROM EM_time_record RC', criterias=criterias, params=params).render()

    @route('/today-status', methods=['GET'])
    @decorators.return_json
    @login_required_json()
    # @api_secret
    def today_status(self, log=None):
        start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = start_day.replace(hour=23, minute=59, second=59)
        rs = SMY().query_row('SELECT  * FROM EM_time_record WHERE locked=0 AND user_id=:user_id AND created_time BETWEEN :start_day AND :end_day',
                             {'user_id': log['id'], 'start_day': start_day, 'end_day': end_day})
        return {'err': 0, 'data': rs}

    @route('/insert', methods=['POST'])
    @decorators.return_json
    @login_required_json(roles=['admin'])
    @api_secret
    def insert(self, log=None):
        data = request.json
        data['locked'] = 0
        data['time_in'] = 1
        data['time_out'] = 1
        data['modified'] = datetime.now()
        data['created_time'] = datetime.now()
        data['user_modified'] = log['id']
        data['user_id'] = log['id'] if not data.get('user_id') else data['user_id']
        company_coords = SMY().query_scalar('SELECT coords, accept_range FROM EM_company WHERE locked=0')
        if company_coords:
            if data.get('coords_in'):
                data['distance_in'] = DistanceUtil().distance_from_str(company_coords, data['coords_in'])
            if data.get('coords_out'):
                data['distance_out'] = DistanceUtil().distance_from_str(company_coords, data['coords_out'])
            rs = SMY().insert(table='EM_time_record', data=data)
            if rs > 0:
                return {'err': 0}
        return {'err': 1}

    @route('/update', methods=['POST'])
    @login_required_json(roles=['admin'])
    @decorators.return_json
    @api_secret
    def update(self, log=None):
        data = dict(
            time_in=request.json.get('time_in'),
            coord_in=request.json.get('coord_in'),
            time_out=request.json.get('time_out'),
            coord_out=request.json.get('coord_out'),
            user_id=log['id'] if not request.json.get('user_id') else request.json['user_id']
        )
        data['modified'] = datetime.now()
        data['user_modified'] = log['id']
        if data['time_out']:
            data['duration'] = data['time_out'] - data['time_in']
        company_coords = SMY().query_scalar('SELECT coords FROM EM_company WHERE locked=0')
        if company_coords:
            if data.get('coord_in'):
                data['distance_in'] = DistanceUtil().distance_from_str(company_coords, data['coord_in'])
            if data.get('coord_out'):
                data['distance_out'] = DistanceUtil().distance_from_str(company_coords, data['coord_out'])
            rs = SMY().update(table='EM_time_record', data=data, where={'id': request.json.get('id')})
            if rs > 0:
                return {'err': 0}
        return {'err': 1}

    def __check_exist_checkin_out(self, user_id, type='checkin'):
        start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = start_day.replace(hour=23, minute=59, second=59)
        rs = SMY().query_row('SELECT  * FROM EM_time_record WHERE locked=0 AND user_id=:user_id AND created_time BETWEEN :start_day AND :end_day',
                             {'user_id': user_id, 'start_day': start_day, 'end_day': end_day})
        print('Not checkin', rs)
        if not rs:
            return False
        if type == 'checkin' and rs['time_in']:
            return True
        if type == 'checkout' and rs['time_out']:
            return True
        return False

    @route('/checkin', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def checkin(self, log=None):
        data = dict(
            time_in=datetime.now(),
            coord_in=request.json.get('coord'),
            user_id=log['id'],
            modified=datetime.now(),
            created_time=datetime.now(),
            user_modified=log['id'],
            created_user=log['id'],
        )
        if self.__check_exist_checkin_out(user_id=log['id'], type='checkin'):
            return {'err': 3, 'msg': 'Exists Checkin today'}
        company = SMY().query_row('SELECT coords, accept_range FROM EM_company WHERE locked=0')
        if company:
            coords = company['coords']
            accept_range = company['accept_range']
            data['distance_in'] = DistanceUtil().distance_from_str(coords, data['coord_in'])
            if data['distance_in'] <= accept_range:
                rs = SMY().insert(table='EM_time_record', data=data)
                data['id'] = rs
                if rs > 0:
                    return {'err': 0, 'data': data}
            else:
                return {'err': 2, 'msg': 'Out of range', 'data': data}
        return {'err': 1, 'msg': 'Error Unkown'}

    @route('/checkout', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def checkout(self, log=None):
        start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = start_day.replace(hour=23, minute=59, second=59)
        data = dict(
            time_out=datetime.now(),
            coord_out=request.json.get('coord'),
            user_id=log['id'],
            start_day=start_day,
            end_day=end_day,
        )
        if self.__check_exist_checkin_out(user_id=log['id'], type='checkout'):
            return {'err': 3, 'msg': 'Exists Checkout today'}
        company = SMY().query_row('SELECT coords, accept_range FROM EM_company WHERE locked=0')
        if company:
            coords = company['coords']
            accept_range = company['accept_range']
            last_checkin = SMY().query_row('SELECT * FROM EM_time_record WHERE user_id=:user_id AND locked=0 AND approved=0 ORDER BY time_in DESC LIMIT 1;', {'user_id': log['id']})
            data['distance_out'] = DistanceUtil().distance_from_str(coords, data['coord_out'])
            data['duration'] = (data['time_out'] - last_checkin['time_in']).total_seconds()
            if data['distance_out'] <= accept_range:
                SMY().execute(
                    'UPDATE EM_time_record SET time_out=:time_out, coord_out=:coord_out,distance_out=:distance_out, duration=:duration WHERE user_id=:user_id AND created_time BETWEEN :start_day AND :end_day',
                    data)
                last_checkin = SMY().query_row('SELECT * FROM EM_time_record WHERE user_id=:user_id AND locked=0 AND approved=0 ORDER BY time_in DESC LIMIT 1;', {'user_id': log['id']})
                return {'err': 0, 'data': last_checkin}
            else:
                return {'err': 2, 'msg': 'Out of Range', 'data': data}
        return {'err': 2, 'data': None}

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
        rs = SMY().update(table='EM_time_record', data=data, where={'id': object_id})
        if rs:
            return {'err': 0}
        return {'err': 1}

    def __extract_ids(self, items):
        return [i['id'] for i in items]

    @route('/bulk-approved', methods=['POST'])
    @decorators.return_json
    @login_required_json()
    @api_secret
    def bulk_receive_idea(self, log=None):
        ids = self.__extract_ids(request.json['items'])
        data = {
            'ids': ids,
            'approved': request.json['data']['approved'],
        }
        rs = SMY().execute('UPDATE EM_time_record SET approved=:approved WHERE id IN :ids', data)
        if rs:
            return {'err': 0}
        return {'err': 1}

    @route('/restore', methods=['POST'])
    @decorators.return_json
    @login_required_json()
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

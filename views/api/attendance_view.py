from flask_classful import FlaskView, route
from common import decorators
from flask import request
from common.sql_table import SqlGrid
from common.authentication import login_required_json, api_secret
from setting import SMY

class AttendanceView(FlaskView):
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

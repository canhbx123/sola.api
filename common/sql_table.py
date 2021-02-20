from flask import request
from pymongo.collection import Collection
from setting import SMY


class SqlGrid:
    def __init__(self, conn, query: str, fromdb: str, criterias: [], total_query: str = 'SELECT COUNT(1)', params=None):
        self.conn = conn
        self.fromdb = fromdb
        self.criterias = criterias
        self.query = query
        self.total_query = total_query
        self.params = params

    def custom_row(self, row):
        return row

    def render(self):
        grid = request.json
        currentPage = int(grid.get('currentPage'))
        perPage = int(grid.get('perPage'))
        offset = (currentPage - 1) * perPage
        sortBy = grid.get('sortBy')
        sortDesc = grid.get('sortDesc')
        sortDesc = 'ASC' if not sortDesc else 'DESC'

        final_query = [self.query + ' ' + self.fromdb + ' WHERE 1=1']
        criteria_sql = ' '.join(self.criterias)
        final_query.append(criteria_sql)
        if sortBy:
            sorts = ['ORDER BY %s' % sortBy, sortDesc]
            final_query.extend(sorts)
        pageing = 'LIMIT %s,%s' % (offset, perPage)
        final_query.append(pageing)
        query = ' '.join(final_query)
        print(query)
        qry_total = ' '.join([self.total_query, self.fromdb, 'WHERE  1=1', criteria_sql])
        total = self.conn.query_scalar(qry_total, self.params, close=False)
        results = self.conn.query_table(query, self.params)
        return {'items': results, 'count': total}

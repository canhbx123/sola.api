from flask import request
from pymongo.collection import Collection
from setting import SMY


class SqlGrid:
    def __init__(self, conn, query: str, fromdb: str, criterias: [], total_query: str = 'SELECT COUNT(1)', params=None, custom_row=None, custom_sort=None):
        self.conn = conn
        self.fromdb = fromdb
        self.criterias = criterias
        self.query = query
        self.total_query = total_query
        self.params = params
        self.custom_row = custom_row
        self.custom_sort = custom_sort

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
        if self.custom_sort:
            final_query.append(self.custom_sort)
        elif sortBy:
            sorts = ['ORDER BY %s' % sortBy, sortDesc]
            final_query.extend(sorts)
        pageing = 'LIMIT %s,%s' % (offset, perPage)
        final_query.append(pageing)
        query = ' '.join(final_query)
        qry_total = ' '.join([self.total_query, self.fromdb, 'WHERE  1=1', criteria_sql])
        total = self.conn.query_scalar(qry_total, self.params, close=False)
        print(query)
        results = self.conn.query_table(query, self.params)
        if self.custom_row:
            for item in results:
                self.custom_row(item)
        return {'items': results, 'count': total}

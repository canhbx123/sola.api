#!/usr/bin/env python3
import os
import re
import copy
import MySQLdb
import MySQLdb.cursors
from datetime import datetime


class Dmysql:
    def __init__(self, host: str, user: str, passwd: str, db: str, port: int = 3306, keep_connect: bool = False):
        self.host, self.port = host, port
        self.user, self.passwd, self.db = user, passwd, db
        self.query, self.__conn, self.keep_connect = '', None, keep_connect
        self.err, self.err_msg, self.allow_log = 0, None, False

    def connecting(self, db=None):
        if not db:
            db = self.db
        # print('MYSQL CONNECTION', db)
        return MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=db, port=self.port,
                               charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)

    def connect(self):
        if not self.__conn:
            self.__conn = self.connecting()
            self._log_file('connection open')
        return self.__conn

    def close(self):
        if not self.keep_connect and self.__conn:
            self.__conn.close()
            self._log_file('connection close')
            self.__conn = None

    def query_scalar(self, query: str, data: dict = None, close: bool = True):
        result, rs = None, self.query_row(query, data, close=close)
        if rs and self.err == 0:
            rs2 = list(rs.values())
            if rs2:
                result = rs2[0]
        return result

    def query_row(self, query: str, data: dict = None, close: bool = True) -> dict:
        result, rs = None, self.execute(query, data)
        if rs and self.err == 0:
            result = rs.fetchone()
        if close:
            self.close()
        return result

    __OPERATORS = {'$eq': '=', '$gt': '>', '$gte': '>=', '$lt': '<', '$lte': '<=', '$ne': '<>'}

    # '$in': ' IN','$nin': ' NOT IN','$and': ' AND ', '$or': ' OR ', '$not': ' NOT ', '$nor': ' NOR'}

    def __dict2keys(self, data: dict) -> list:
        result = []
        for k, v in data.items():
            _operator = '='
            if isinstance(v, dict):
                for _k, _v in v.items():
                    if _k in self.__OPERATORS:
                        _operator = self.__OPERATORS[_k]
            result.append('%s%s%s' % (self.__prefix_field(k), _operator, self._dict_value(k)))
        return result

    def _qargs(self, qry: str, data: dict) -> str:
        for k, v in data.items():
            qry = re.sub(r':%s(\s+|\)|$|;|:|,|\+|-|\*|/)' % k, r'%s\1' % self._dict_value(k), qry)
        # print('qry=', qry)
        return qry

    def chk_has(self, table: str, where: dict = None, close: bool = True, query: str = None) -> bool:
        if not query:
            where_query = ''
            if where:
                where_query = ' WHERE %s' % ' AND '.join(self.__dict2keys(where))
            query = 'SELECT 1 FROM %s%s' % (table, where_query)
        nquery = 'SELECT EXISTS(%s) AS has;' % query
        result = self.query_scalar(nquery, data=where, close=close)
        if result:
            return result > 0
        return False

    def query_table(self, query: str, data: dict = None, close: bool = True) -> list:
        result, rs = None, self.execute(query, data)
        if rs and self.err == 0:
            result = rs.fetchall()
        if close:
            self.close()
        return result

    @staticmethod
    def _dict_value(key):
        return '%(' + str(key) + ')s'

    def shell_exec(self, command: str):
        return os.system("mysql -u%s -p'%s' %s" % (self.user, self.passwd, command))
        # _args = ['mysql', 'u%s' + self.user, 'p%s' + self.passwd, command]
        # return subprocess.Popen(_args, stdout=subprocess.PIPE).communicate()

    def database_create(self, dbname: str = None):
        if not dbname:
            dbname = self.db
        self.shell_exec('-e "CREATE DATABASE IF NOT EXISTS %s;"' % dbname)

    def database_exists(self, dbname: str):
        cur = self.connecting('INFORMATION_SCHEMA').cursor()
        return cur.execute("SELECT SCHEMA_NAME FROM SCHEMATA WHERE SCHEMA_NAME=\'%s\';" % dbname) == 1

    def insert(self, table: str, data: dict, commit: bool = True, close: bool = True) -> int:
        fields = [self.__prefix_field(k) for k in data.keys()]
        query = 'INSERT INTO %s (%s) VALUES (%s);' % (
            table, ','.join(fields), ','.join(map(self._dict_value, data)))
        result, rs = -1, self.execute(query, data, commit=commit, regquery=False)
        if rs and self.err == 0:
            result = rs.lastrowid
        if close:
            self.close()
        return result

    @staticmethod
    def __prefix_field(field: str) -> str:
        return '`%s`' % field

    def _where4update(self, table: str, data: dict, where: dict = None):
        if data and isinstance(data, dict):
            # sets = ['%s=%s' % (self.__prefix_field(k), self._dict_value(k)) for k, v in data.items()]
            _qry = 'UPDATE %s SET %s' % (table, ','.join(self.__dict2keys(data)))
            if where:
                _dt, wheres = copy.copy(data), []
                for k, v in where.items():
                    dk = k
                    if k in _dt.keys():
                        dk += 'dragonupdate'
                    _dt[dk] = v
                    wheres.append('%s=%s' % (self.__prefix_field(k), self._dict_value(dk)))
                return _qry + ' WHERE %s;' % ' AND '.join(wheres), _dt
            return _qry + ';', data

    def update(self, table: str = None, data: dict = None, where: dict = None, commit: bool = True, close: bool = True, query: str = None) -> int:
        result = -1
        if not query:
            query, _data = self._where4update(table, data, where=where)
            rs = self.execute(query, _data, commit=commit, regquery=False)
        else:
            rs = self.execute(query, data, commit=commit, regquery=True)
        if rs and self.err == 0:
            result = rs.rowcount
        if close:
            self.close()
        return result

    def delete(self, table: str = None, where: dict = None, commit: bool = True, close: bool = True, query: str = None) -> int:
        result = -1
        if not query:
            query = 'DELETE FROM %s' % table
            if where:
                # wheres = ['%s=%s' % (self.__prefix_field(k), self._dict_value(k)) for k, v in where.items()]
                query += ' WHERE %s;' % ' AND '.join(self.__dict2keys(where))
            rs = self.execute(query, where, commit=commit, regquery=False)
        else:
            rs = self.execute(query, where, commit=commit, regquery=True)
        if rs and self.err == 0:
            result = 1
        if close:
            self.close()
        return result

    def _log_file(self, message: str, data: dict = None):
        if self.allow_log:
            tnow = datetime.now()
            qfile = tnow.strftime('%m_%d_%H')
            import json
            with open('/home/dll/mysql/%s_%s.sql' % (self.db, qfile), 'a') as cw:
                cw.write('\n/*%s*/\t%s\n' % (tnow.strftime('%H:%M:%S'), message))
                if data:
                    cw.write('%s\n' % json.dumps(data))

    def commit(self):
        try:
            self.connect().commit()
            self.err = 0
        except Exception as e:
            self.err = 500
            self.err_msg = str(e)
            print('ERR SQL', self.err_msg)

    def execute(self, query: str, data: dict = None, commit: bool = True, regquery: bool = True):
        # print('execute query=', query)
        # print('execute data=', data)
        if not query:
            self.err = 502
            self.err_msg = 'query is empty'
        else:
            if data and regquery:
                query = self._qargs(query, data)
            self.query = query
            try:
                conn = self.connect()
                csr = conn.cursor()
                if data:
                    for k, v in data.items():
                        if isinstance(v, dict):
                            for _k, _v in v.items():
                                if _k in self.__OPERATORS:
                                    data[k] = _v
                # print('QRY=', self.query, data)
                csr.execute(self.query, data)
                if commit:
                    conn.commit()
                self.err = 0
                self._log_file(self.query, data)
                return csr
            except Exception as e:
                self.err = 500
                self.err_msg = str(e)
                print('ERR SQL', self.err_msg)
                # print(self.query, data)

    def __execute_table(self, query: str, close: bool = True) -> int:
        result, rs = -1, self.execute(query)
        if rs and self.err == 0:
            result = 1
        if close:
            self.close()
        return result

    def truncate(self, table: str, close: bool = True) -> int:
        return self.__execute_table('TRUNCATE TABLE %s;' % table, close)

    def droptable(self, table: str, close: bool = True) -> int:
        return self.__execute_table('DROP TABLE %s;' % table, close)

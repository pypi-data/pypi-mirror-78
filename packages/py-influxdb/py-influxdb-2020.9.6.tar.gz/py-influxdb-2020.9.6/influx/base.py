import os
from logging import info
from urllib.parse import urljoin

import requests


class BaseClient(object):

    def __init__(self, host, port=8086, use_ssl=False, is_dns=False, user=None, password=None):
        """
        Authenticates and creates a session to be used for DB operations
        :param host: the host name
        :param port: the port to be used, defaults to 8086. Unused if is_dns is set to True
        :param use_ssl: indicates use SSL/TLS if True, False otherwise. Defaults to False
        :param is_dns: indicates if host represents DNS and not an IP/localhost. Defaults to False
        :param user: the user name to be used. Authentication is enabled if specified
        :param password: the password to be used in combination to user name. Used only if user name is specified
        """
        scheme = 'https' if use_ssl else 'http'
        host = host if is_dns else f'{host}:{port}'
        self._url = f'{scheme}://{host}'
        self._user = user or os.environ.get('INFLUX_DB_USER')
        self._password = password or os.environ.get('INFLUX_DB_PASSWORD')
        info(f'Client configured with base URL: {self._url}')

    def query(self, query, db=None):
        """
        Executes the query provided
        :param query: the query to be executed
        :param db: the db name to query against
        :return: response returned
        """
        url = urljoin(self._url, 'query')
        info(f'Invoking URL: {url}: Query: {query}')
        params = BaseClient.get_params(query, db)
        return requests.post(url, auth=(self._user, self._password), params=params)

    @staticmethod
    def get_params(query, db):
        params = {'q': query}
        params.update({'db': db} if db else {})
        return params


class Query(object):

    def __init__(self):
        self._select = list()
        self._functions = list()
        self._where = list()
        self._group_by = list()
        self._measure = None

    def select(self, cols):
        """
        Columns to be part of the select clause
        :param cols: list of columns
        """
        self._select.extend([f'"{col}"' for col in cols])
        return self

    def select_functions(self, name, col):
        """
        Name of the function and col name on which the functions needs to aggregate
        :param name: the function name, SUM, COUNT, etc
        :param col: the
        """
        self._functions.append(f'{name}("{col}")')
        return self

    def measure(self, name):
        """ The measure name """
        self._measure = f'"{name}"'
        return self

    def where(self, col, val, op='='):
        """
        The where clause for the query
        :param col: the column name
        :param op: the operation to compare '=', '<', etc
        :param val: the value to filter
        """
        self._where.append(Query._expression(col, op, val))
        return self

    def and_(self, col, val, op='='):
        """
        AND condition to be appended
        :param col: the column name
        :param op: the operation to compare '=', '<', etc
        :param val: the value
        """
        assert self._where, "Cannot add operation without WHERE condition"
        self._where.append(f'AND {Query._expression(col, op, val)}')
        return self

    def or_(self, col, val, op='='):
        """
        OR condition to be appended
        :param col: the column name
        :param op: the operation to compare '=', '<', etc
        :param val: the value
        """
        assert self._where, "Cannot add operation without WHERE condition"
        self._where.append(f'OR {Query._expression(col, op, val)}')
        return self

    def group_by(self, cols):
        """
        Appends a group by clause to the query
        :param cols: the columns on which we want to group_by
        """
        self._group_by.extend([f'"{col}"' for col in cols])
        return self

    def group_by_interval(self, interval='5m'):
        """
        Groups the time series together with 5 minute interval
        :param interval: the interval to group by
        """
        self._group_by.append(f'time({interval})')
        return self

    def build(self):
        """ Builds the final Influx QL query """
        select = ', '.join(self._select) if self._select else '*'
        select = ', '.join(self._functions) if self._functions and not self._select else select
        where = ' '.join(self._where)
        where = f'WHERE {where}' if where else ''
        group_by = ', '.join(self._group_by)
        group_by = f'GROUP BY {group_by}' if self._group_by else ''
        query = f'SELECT {select} FROM {self._measure} {where} {group_by}'
        return query.strip()

    @staticmethod
    def _expression(col, op, val):
        if isinstance(val, str):
            expn = f'"{col}" {op} \'{val}\''
        elif col == 'time':
            expn = f'{col} {op} {val}'
        else:
            expn = f'"{col}" {op} {val}'
        return expn

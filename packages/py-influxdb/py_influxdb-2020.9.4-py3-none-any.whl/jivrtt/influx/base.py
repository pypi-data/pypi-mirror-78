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
        self._where = list()
        self._measure = None

    def select(self, cols):
        """
        Columns to be part of the select clause
        :param cols: list of columns
        """
        self._select.extend(cols)
        return self

    def measure(self, name):
        """ The measure name """
        self._measure = name
        return self

    def where(self, col, val):
        """
        The where clause for the query
        :param col: the column name
        :param val: the value to filter
        """
        self._where.append((None, col, val))
        return self

    def and_(self, col, val):
        """
        AND condition to be appended
        :param col: the column name
        :param val: the value
        """
        assert self._where, "Cannot add operation without WHERE condition"
        self._where.append(('AND', col, val))
        return self

    def or_(self, col, val):
        """
        OR condition to be appended
        :param col: the column name
        :param val: the value
        """
        assert self._where, "Cannot add operation without WHERE condition"
        self._where.append(('OR', col, val))
        return self

    def build(self):
        """ Builds the final Influx QL query """
        is_project_specific_cols = bool(self._select)
        select = '","'.join(self._select) if is_project_specific_cols else '*'
        select = f'"{select}"' if is_project_specific_cols else select
        where = ' '.join(
            [f'"{c}"=\'{v}\'' if i == 0 else f'{o} "{c}"=\'{v}\'' for i, (o, c, v) in enumerate(self._where)])
        where = f'WHERE {where}' if where else ''
        return f'SELECT {select} FROM "{self._measure}" {where}'

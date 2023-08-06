import logging
from logging import info
from urllib.parse import urljoin

import requests

from jivrtt.influx.base import BaseClient, Query


class InfluxQLClient(BaseClient):

    def __init__(self, host, port=8086, use_ssl=False, is_dns=False, user=None, password=None):
        """
        DB Client using Influx QL for interacting
        :param host: the host name
        :param port: the port to be used, defaults to 8086. Unused if is_dns is set to True
        :param use_ssl: indicates use SSL/TLS if True, False otherwise. Defaults to False
        :param is_dns: indicates if host represents DNS and not an IP/localhost. Defaults to False
        :param user: the user name to be used. Authentication is enabled if specified
        :param password: the password to be used in combination to user name. Used only if user name is specified
        """
        super().__init__(host, port, use_ssl=use_ssl, is_dns=is_dns, user=user, password=password)

    def create_db(self, name):
        """
        Creates a database with the given name
        :param name: the db name
        """
        query = f'CREATE DATABASE {name}'
        self.query(query)

    def get(self, query, db=None):
        """
        Executes GET query
        :param query: the query
        :param db: the db
        :return: response returned
        """
        url = urljoin(self._url, 'query')
        info(f'Invoking URL: {url}: Query: {query}')
        params = BaseClient.get_params(query, db)
        return requests.get(url, auth=(self._user, self._password), params=params)

    def write(self, db, measure, field, value, tags=None, timestamp=None):
        """
        Executes a write query to DB
        :param measure: the measure name
        :param field: the field key
        :param value: the field value
        :param db: the db name to query against
        :param tags: dict of tags to be saved against the point
        :param timestamp: the timestamp in nanoseconds from epoch time
        :return: response from server
        """
        return self.write_many_fields(db, measure, {field: value}, tags=tags, timestamp=timestamp)

    def write_many_fields(self, db, measure, value_by_field, tags=None, timestamp=None):
        """
        Executes a write query to DB
        :param measure: the measure name
        :param value_by_field: the value by field
        :param db: the db name to query against
        :param tags: dict of tags to be saved against the point
        :param timestamp: the timestamp in nanoseconds from epoch time
        :return: response from server
        """
        url = urljoin(self._url, 'write')
        tags = tags or dict()
        tags = ','.join(f'{tn}={tv}' for tn, tv in tags.items())
        fields = ','.join(f'{f}={v}' for f, v in value_by_field.items())
        data = f"{measure}{f',{tags}' if tags else ''} {fields} {timestamp or ''}".strip()
        info(f'Invoking URL: {url}: Query: {data}')
        return requests.post(url, auth=(self._user, self._password), data=data, params={'db': db})

    def fetch(self, db, query_inst: Query):
        """
        Gets all the rows matching the query instance
        :param db: the db name
        :param query_inst: the query instance
        :return: response as returned from the API
        """
        q = query_inst.build()
        return self.query(q, db=db)

    def fetch_all(self, db, measure):
        """
        Gets all the rows for the given measure
        :param db: the db name
        :param measure: the measure which you want to retrieve
        :return: response as returned from the API
        """
        q = Query().measure(measure).build()
        return self.query(q, db=db)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = InfluxQLClient('192.168.99.100')
    # info(client.create_db('test_db'))
    # write_resp = client.write('test_db', 'sample', 'val', 1.005, tags={'tag1': 'tag1Val', 'tag2': 'tag2Val'})
    # write_resp = client.write('test_db', 'sample', 'val', 1.005, tags={'tag1': 'tag3Val', 'tag2': 'tag4Val'})
    # write_resp = client.write_many_fields(
    #     'test_db',
    #     'sample', {
    #         'new_val': 1.007,
    #         'val': 1.01
    #     },
    #     tags={
    #         'tag1': 'tag3Val',
    #         'tag2': 'tag4Val',
    #     }
    # )
    # print(write_resp)
    # query = Query().measure('sample').select(['val', 'tag1', 'tag2']).where('tag1', 'tag1Val')
    # query = Query().measure('sample').select(['val', 'new_val', 'tag1', 'tag2'])
    # all_rows = client.fetch('test_db', query)
    query = Query().measure('price').select(['sym', 'inst', 'low', 'vol', 'prc']).where('quote', 'USDT').and_('base',
                                                                                                              'CRO')
    # query = Query().measure('price')
    all_rows = client.fetch('ta', query)
    # all_rows = client.fetch_all('ta', 'price')
    print(all_rows.json())

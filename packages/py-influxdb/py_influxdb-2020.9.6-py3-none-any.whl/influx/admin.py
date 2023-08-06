import logging

from influx.base import BaseClient


class InfluxAdminClient(BaseClient):

    def __init__(self, host, port=8086, use_ssl=False, is_dns=False, admin_user=None, admin_pwd=None):
        """
        Contains APIs for all the admin related query of user creation and privilege management.
        Requires an authenticated session from another user
        :param host: the host name
        :param port: the port to be used, defaults to 8086. Unused if is_dns is set to True
        :param use_ssl: indicates use SSL/TLS if True, False otherwise. Defaults to False
        :param is_dns: indicates if host represents DNS and not an IP/localhost. Defaults to False
        :param admin_user: the admin user to be used for authentication. Enables authentication.
        :param admin_pwd: the admin password to be used
        """
        super().__init__(host, port, use_ssl, is_dns, user=admin_user, password=admin_pwd)

    def create_user(self, user, password, is_admin=False):
        """
        Creates a new user in DB
        :param user: the user name
        :param password: the password for the user
        :param is_admin: created as an admin user if True, False otherwise. Defaults to False
        :return: response returned by the API
        """
        query = f"CREATE USER {user} WITH PASSWORD '{password}'{' WITH ALL PRIVILEGES' if is_admin else ''}"
        return self.query(query)

    def grant_all_privileges(self, user):
        """
        Grants all privileges to an existing user, elevating user to an admin user
        :param user: the user to be granted privileges
        :return: response returned by the API
        """
        query = f'GRANT ALL PRIVILEGES TO {user}'
        self.query(query)

    def revoke_all_privileges(self, user):
        """
        Revokes all privileges from an existing user
        :param user: the user to be revoked all privileges
        :return: response returned by the API
        """
        query = f'REVOKE ALL PRIVILEGES FROM {user}'
        self.query(query)

    def show_grants(self, user):
        """
        Shows all the grants existing for an user
        :param user: the user name
        :return: response from API
        """
        query = f'SHOW GRANTS FOR {user}'
        return self.query(query)

    def grant_privilege_on_db(self, db, user, privilege):
        """
        Grants specified privilege to user on DB
        :param db: the db name
        :param user: the user name
        :param privilege: the privilege to be provided
        :return: response from API
        """
        query = f'GRANT {privilege} ON {db} TO {user}'
        self.query(query)

    def _revoke_privilege(self, db, user, privilege):
        """
        Revokes specified privilege to user on DB
        :param db: the db name
        :param user: the user name
        :param privilege: the privilege to be revoked
        :return: response from API
        """
        query = f'REVOKE {privilege} ON {db} TO {user}'
        self.query(query)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    a_client = InfluxAdminClient('192.168.99.100', admin_user='admin', admin_pwd='admin')
    response = a_client.create_user('nkm', 'nkm', is_admin=True)
    print(response.status_code)
    print(response.json())

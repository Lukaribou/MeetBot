import mariadb
import sys


class DataBase:
    def __init__(self, user: str, password: str, host: str, port: int):
        self._conn = None
        try:
            self._conn = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                autocommit=True)
        except mariadb.Error as e:
            print(f'Error connecting to DataBase: {e}')
            sys.exit(1)

        self.cursor = self._conn.cursor()

    def disconnect(self):
        print(f'Déconnection de la base de données...')
        self._conn.close()

import mariadb
import sys
from typing import Tuple, Union

from meetbot.config import DB_USER, DB_PSWD


# https://mariadb.com/docs/appdev/connector-python/
class DataBase:
    def __init__(self, host: str, port: int, database: str):
        self._conn = None
        try:
            self._conn = mariadb.connect(
                user=DB_USER,
                password=DB_PSWD,
                host=host,
                port=port,
                database=database,
                autocommit=True)
        except mariadb.Error as e:
            print(f'Error connecting to DataBase: {e}')
            sys.exit(1)

        self.cursor = self._conn.cursor(named_tuple=True)

    def disconnect(self) -> None:
        print(f'Déconnection de la base de données...')
        self._conn.close()

    def execute(self, cmd: str, *args):
        self.cursor.execute(cmd, args)
        return self.cursor

    def profile_exist(self, author_id):
        return len(self.execute("SELECT * FROM profiles WHERE user_id = ?", str(author_id)).fetchall()) != 0

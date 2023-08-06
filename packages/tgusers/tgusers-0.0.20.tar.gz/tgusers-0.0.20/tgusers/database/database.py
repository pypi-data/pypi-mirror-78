import psycopg2
import psycopg2.extras
import psycopg2.errors


from dataclasses import dataclass


@dataclass
class PostgresAuthData:
    dbname: str
    user: str
    password: str
    host: str
    port: int


def make_dict_rows(rows: list) -> list:
    dict_list = []
    for row in rows:
        dict_list.append(dict(row))
    return dict_list


class DataBase:
    def __init__(self, pg_auth_data: PostgresAuthData):
        self.conn: psycopg2._psycopg._connect = None
        self.cursor = None
        self.pg_auth_data = pg_auth_data
        self.connect()


    def connect(self):
        self.conn = psycopg2.connect(dbname=self.pg_auth_data.dbname, user=self.pg_auth_data.user, password=self.pg_auth_data.password,
                                     host=self.pg_auth_data.host, port=self.pg_auth_data.port)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    def reconnect(self):
        self.disconnect()
        self.connect()

    def commit(self):
        self.conn.commit()

    def request(self, sql_request, args: tuple = None):
        try:
            if args:
                self.cursor.execute(sql_request, args)
            else:
                self.cursor.execute(sql_request)
        except psycopg2.errors.InFailedSqlTransaction:
            self.reconnect()
            if args:
                self.cursor.execute(sql_request, args)
            else:
                self.cursor.execute(sql_request)
        # try:
        if self.cursor.description:
            return make_dict_rows(self.cursor.fetchall())
        # except psycopg2.ProgrammingError:
        #     return None

    def __del__(self):
        self.disconnect()


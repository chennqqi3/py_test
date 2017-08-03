import warnings

import MySQLdb
from sqlalchemy import create_engine

import config_default

warnings.filterwarnings('ignore', category=MySQLdb.Warning)
db_url = config_default.db_url
dev_db_url = 'mysql://admin:admin1234@192.168.5.87:3306/test?charset=utf8'
db_product_url = 'mysql://admin:admin2048az@192.168.50.95:3306/test?charset=utf8'


class SQLQuery(object):
    def __init__(self, engine):
        self.engine = engine
        self.record = {}
        self.lastInsertID = None
        self.affectedRows = None
        self.rowcount = None

    def Query(self, query):
        conn = self.engine.connect()
        try:
            result = conn.execute(query)
            if result.returns_rows:
                self.record = result
            self.affectedRows = result.rowcount
            self.rowcount = result.rowcount
            self.lastInsertID = result.lastrowid
        finally:
            if conn is not None:
                conn.close()

    def call_proc(self, query):
        connection = self.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc(query)
            cursor.close()
            connection.commit()
        finally:
            connection.close()


def get_query():
    return SQLQuery(create_engine(db_url))


def get_dev_query():
    return SQLQuery(create_engine(dev_db_url))


def get_product_query():
    return SQLQuery(create_engine(db_product_url))

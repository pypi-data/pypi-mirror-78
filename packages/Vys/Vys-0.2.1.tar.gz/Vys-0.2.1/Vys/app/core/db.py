#! python3
import mysql.connector

from Vys.app.errors import *
from Vys.app.core.datetime_apps import DatetimeConstruct, DatetimeGenerator

import sqlite3

import string
import secrets

from datetime import datetime


class DbCredentials:
    def __init__(
            self,
            host=None,
            port=None,
            user=None,
            auth_plugin='mysql_native_password',
            password=None,
            database=None
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def mysql_connect(self):
        db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            auth_plugin='mysql_native_password',
            passwd=self.password,
            database=self.database
        )
        return db

    def sqlite_connect(self):
        db = sqlite3.connect(self.database)
        return db


class MysqlModel:
    def __init__(self, db_credentials, table, f_keys):
        self.db_name = db_credentials.database
        self.db = db_credentials.mysql_connect()
        self.table = table
        self._parameters = {'ID': {}}
        self._required = []
        self.validator = Validator()
        self._table_check(f_keys)

    def _table_check(self, f_keys):
        if self.table not in self._tables:
            cursor = self.db.cursor()
            sql = f"CREATE TABLE {self.table} (ID varchar(9) NOT NULL UNIQUE, createdAt DATETIME, updatedAt DATETIME"
            if f_keys:
                sql += f", {f_keys['column']} VARCHAR(9)"

                sql += f", PRIMARY KEY (ID)"

                sql += f", FOREIGN KEY ({f_keys['column']}) REFERENCES {f_keys['table']}({f_keys['foreign column']}))"
            else:
                sql += f", PRIMARY KEY (ID))"
            cursor.execute(sql)

    def find_one(self, query, fetch='*'):
        cursor = self.db.cursor(buffered=True)
        sql = f"SELECT {fetch} FROM {self.table}"
        val = list()
        for item in query:
            self._validate_params(item, message='Enter real field')

            sql += f" WHERE {item} = %s" if 'WHERE' not in sql else f" AND {item} = %s"
            val.append(query[item], )

        cursor.execute(sql, val)
        result = cursor.fetchone()
        if not result:
            raise DbError(
                message='Your query produced 0 results. '
            )
        total_result = {}

        zipped_result = zip(self._columns(), result) if fetch == '*' else zip([i for i in fetch.split(', ')], result)

        for key, value in zipped_result:
            total_result[key] = value

        return total_result

    def find(self, query, fetch='*', table=None):
        table = table or self.table
        cursor = self.db.cursor()
        sql = f"SELECT {fetch} FROM {table}"
        val = list()
        for item in query:
            self._validate_params(item, 'Enter real field', table=table)

            sql += f" WHERE {item} = %s" if 'WHERE' not in sql else f" AND {item} = %s"
            val.append(query[item], )

        cursor.execute(sql, val)
        result_from_fetch = cursor.fetchall()

        total_result = []

        for row in result_from_fetch:
            result = {}
            zipped_result = zip(getattr(self, '_columns')(table), row) if fetch == '*' else zip([i for i in fetch.split(', ')], row)
            for key, value in zipped_result:
                result[key] = value
            total_result.append(result)

        return total_result

    def create(self, query):
        cursor = self.db.cursor()
        date = DatetimeGenerator()
        new_id = _create_id()
        val = [new_id, str(date), str(date)]
        cols_to_insert = 'ID, CreatedAt, UpdatedAt'
        inserts = '%s, %s, %s'
        for count, item in enumerate(query):
            self._validate_params(item, message='Enter real field')
            self._validate(category=item, val=query[item])

            val.append(query[item])

            cols_to_insert += f', {item}'
            inserts += ', %s'

        for requirement in self._required:
            if requirement not in cols_to_insert:
                raise Exception(f'Requirement: {requirement} unsatisfied. ')

        sql = f"INSERT INTO {self.table} ({cols_to_insert}) VALUES ({inserts})"
        cursor.execute(sql, val)
        self.db.commit()
        x = self.find_one(query={'ID': new_id})
        return x

    def find_and_update(self, query, update):
        cursor = self.db.cursor()
        sql = f"UPDATE {self.table} SET UpdatedAt = %s"
        date = DatetimeGenerator()
        val = [str(date)]
        for count, param in enumerate(update):
            self._validate_params(param, 'Column doesnt Exist')

            sql += f", {param} = %s"
            val.append(update[param])

        sql += " WHERE "
        for count, item in enumerate(query):
            self._validate_params(item, 'Column doesnt Exist')

            sql += f"{item} = %s" if count == 0 else f" AND {item} = %s"
            val.append(query[item])
        cursor.execute(sql, val)
        self.db.commit()

    def _validate_params(self, item, message, **kwargs):
        if 'table' in kwargs:
            return
        if item == '_ROWID_' or item == 'rowid' or item == 'ROWNUM':
            return
        if item not in self._parameters:
            raise DbError(f'{message} - {item}')

    def _columns(self, table=None):
        table = table or self.table
        cursor = self.db.cursor(buffered=True)
        sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{self.db_name}' AND " \
              f"TABLE_NAME='{table}';"
        cursor.execute(sql)
        cols = cursor.fetchall()
        columns = [col[0] for col in cols]
        return columns

    @property
    def _tables(self):
        cursor = self.db.cursor()
        sql = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{self.db_name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        tables = [table[0] for table in result]
        return tables

    def _validate(self, category, val):

        self.validations = {
            'min_length': self.validator.min_length,
            'required': self.validator.required,
            'dbtype': self.validator.dbtype,
            'type': self.validator.type,
            'FOREIGN_KEY': self.validator.FOREIGN_KEY
        }

        for parameter in self._parameters[category]:
            self.validations[parameter](val, self._parameters[category][parameter])

    def _create_column(self, col_name, col_type='TEXT(255)', options=None):
        cursor = self.db.cursor()
        sql = f"ALTER TABLE {self.table} ADD {col_name} {col_type}"
        cursor.execute(sql)
        self.db.commit()
        if options is not None and 'FOREIGN_KEY' in options:
            cursor = self.db.cursor()
            sql = f"ALTER TABLE {self.table} ADD FOREIGN KEY ({col_name}) REFERENCES {options['FOREIGN_KEY']['ref']}(ID)"
            cursor.execute(sql)
            self.db.commit()


class SqLiteModel:
    def __init__(self, db_credentials, table, f_keys):
        self.db_name = db_credentials.database
        self.db = db_credentials.sqlite_connect()
        self.table = table
        self._parameters = {'ID': {}}
        self._required = []
        self.validator = Validator()
        self._table_check(f_keys)

    def _table_check(self, f_keys):
        if self.table not in self._tables:
            cursor = self.db.cursor()
            sql = f"CREATE TABLE {self.table} (ID varchar(9) NOT NULL UNIQUE, createdAt DATETIME, updatedAt DATETIME"
            if f_keys:
                sql += f", {f_keys['column']} VARCHAR(9)"

                sql += f", PRIMARY KEY (ID)"

                sql += f", FOREIGN KEY ({f_keys['column']}) REFERENCES {f_keys['table']}({f_keys['foreign column']}))"
            else:
                sql += f", PRIMARY KEY (ID))"
            cursor.execute(sql)

    def find_one(self, query, fetch='*'):
        cursor = self.db.cursor()
        sql = f"SELECT {fetch} FROM {self.table}"
        val = list()
        for item in query:
            self._validate_params(item, message='Enter real field')

            sql += f" WHERE {item} = ?" if 'WHERE' not in sql else f" AND {item} = ?"
            val.append(query[item], )

        cursor.execute(sql, val)
        result = cursor.fetchone()
        if not result:
            raise DbError(
                message='Your query produced 0 results. '
            )
        total_result = {}

        zipped_result = zip(self._columns(), result) if fetch == '*' else zip([i for i in fetch.split(', ')], result)

        for key, value in zipped_result:
            total_result[key] = value

        return total_result

    def find(self, query, fetch='*', table=None):
        table = table or self.table
        cursor = self.db.cursor()
        sql = f"SELECT {fetch} FROM {table}"
        val = list()
        for item in query:
            self._validate_params(item, 'Enter real field', table=table)

            sql += f" WHERE {item} = ?" if 'WHERE' not in sql else f" AND {item} = ?"
            val.append(query[item], )

        cursor.execute(sql, val)
        result_from_fetch = cursor.fetchall()

        total_result = []

        for row in result_from_fetch:
            result = {}
            zipped_result = zip(getattr(self, '_columns')(table), row) if fetch == '*' else zip([i for i in fetch.split(', ')], row)
            for key, value in zipped_result:
                result[key] = value
            total_result.append(result)

        return total_result

    def create(self, query):
        new_id = _create_id()
        cursor = self.db.cursor()
        date = DatetimeGenerator()
        val = [new_id, str(date), str(date)]
        cols_to_insert = 'ID, CreatedAt, UpdatedAt'
        inserts = '?, ?, ?'
        for count, item in enumerate(query):
            self._validate_params(item, message='Enter real field')
            self._validate(category=item, val=query[item])

            val.append(query[item])

            cols_to_insert += f', {item}'
            inserts += ', ?'

        for requirement in self._required:
            if requirement not in cols_to_insert:
                raise Exception(f'Requirement: {requirement} unsatisfied. ')

        sql = f"INSERT INTO {self.table} ({cols_to_insert}) VALUES ({inserts})"
        cursor.execute(sql, val)
        self.db.commit()
        # new_sql = f"SELECT * FROM {self.table} WHERE _ROWID_ = {cursor.lastrowid}"
        # cursor.execute(new_sql)
        # x = cursor.fetchall()
        x = self.find_one(query={'_ROWID_': cursor.lastrowid})
        return x

    def find_and_update(self, query, update):
        cursor = self.db.cursor()
        sql = f"UPDATE {self.table} SET UpdatedAt = ?"
        date = DatetimeGenerator()
        val = [str(date)]
        for count, param in enumerate(update):
            self._validate_params(param, 'Column doesnt Exist')

            sql += f", {param} = ?"
            val.append(update[param])

        sql += " WHERE "
        for count, item in enumerate(query):
            self._validate_params(item, 'Column doesnt Exist')

            sql += f"{item} = ?" if count == 0 else f" AND {item} = ?"
            val.append(query[item])
        cursor.execute(sql, val)
        self.db.commit()

    def _validate_params(self, item, message, **kwargs):
        if 'table' in kwargs:
            return
        if item == '_ROWID_':
            return
        if item not in self._parameters:
            raise DbError(f'{message} - {item}')

    def _columns(self, table=None):
        table = table or self.table
        cursor = self.db.cursor()
        sql = f"PRAGMA table_info({table})"
        cursor.execute(sql)
        cols = cursor.fetchall()
        columns = [col[1] for col in cols]
        return columns

    @property
    def _tables(self):
        cursor = self.db.cursor()
        sql = f"SELECT name FROM sqlite_master WHERE type='table'"
        cursor.execute(sql)
        result = cursor.fetchall()
        tables = [table[0] for table in result]
        return tables

    def _validate(self, category, val):

        self.validations = {
            'min_length': self.validator.min_length,
            'required': self.validator.required,
            'dbtype': self.validator.dbtype,
            'type': self.validator.type,
            'FOREIGN_KEY': self.validator.FOREIGN_KEY
        }

        for parameter in self._parameters[category]:
            self.validations[parameter](val, self._parameters[category][parameter])

    def _create_column(self, col_name, col_type='TEXT(255)', options=None):
        cursor = self.db.cursor()
        sql = f"ALTER TABLE {self.table} ADD {col_name} {col_type}"
        cursor.execute(sql)
        self.db.commit()
        if options is not None and 'FOREIGN_KEY' in options:
            cursor = self.db.cursor()
            sql = f"ALTER TABLE {self.table} ADD FOREIGN KEY ({col_name}) REFERENCES {options['FOREIGN_KEY']['ref']}(ID)"
            cursor.execute(sql)
            self.db.commit()


class Validator:
    def __init__(self):
        pass

    @staticmethod
    def min_length(value, option):
        if len(value) < option:
            raise DbError('Password too short')

    @staticmethod
    def required(value, option):
        pass

    @staticmethod
    def dbtype(value, option):
        pass

    @staticmethod
    def type(value, option):
        if not isinstance(value, option):
            raise DbError('Wrong Type!')

    @staticmethod
    def FOREIGN_KEY(value, option):
        pass


def _create_id():
    alphabet = string.ascii_letters + string.digits
    _id = ''.join(secrets.choice(alphabet) for u in range(9))
    return _id

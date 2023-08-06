#! python3
from Vys.app.core.db import SqLiteModel, MysqlModel

from Vys.app.errors import *


class Virtual:
    def __init__(self):
        self._cols = []
        self._ids = []

    def apply_row(self, row):
        self._ids.append(row['ID'])
        setattr(self, row['ID'], row)

    def __str__(self):
        return str([getattr(self, id) for id in self._ids])


class MySqlSchema(MysqlModel):
    def __init__(self, db_credentials, table, f_keys=None):
        super().__init__(db_credentials, table, f_keys)
        self._parameters = {}
        self._attrs = []
        self._virtual = None
        self.virtual = Virtual()
        self._expand_param = {}

    def init_schema(self, method, params):
        if len(method) != 0:
            create = getattr(self, method[0])(params)
            self.populate({'ID': create['ID']})

    def add_param(self, name, options=None):
        if options is None:
            options = {}
        self._parameters[name] = options

    def add_params(self, names):
        columns = self._columns()
        names['ID'] = {}
        setattr(self, 'createdAt', None)
        setattr(self, 'updatedAt', None)
        self._attrs.append('createdAt')
        self._attrs.append('updatedAt')
        for option in names:
            setattr(self, option, None)
            self._attrs.append(option)
            if option not in columns:
                self._create_column(
                    col_name=option, options=names[option]
                ) if 'dbtype' not in names[option] else self._create_column(
                    col_name=option, col_type=names[option]['dbtype'], options=names[option]
                )
            self._parameters[option] = names[option]
            for item in names[option]:
                if 'required' in item:
                    self._required.append(option)

    def expand_param(self, *args, **kwargs):
        kwargs['fetch'] = '*' if 'fetch' not in kwargs else kwargs['fetch']
        self._expand_param[kwargs['param']] = kwargs['fetch']

    def add_virtual(self, virtual):
        self._virtual = virtual

    def populate_virtual(self):
        query = {
            self._virtual['foreign_column']: getattr(self, self._virtual['field'])
        }

        result = self.find(query=query, table=self._virtual['table'])

        for row in result:
            self.virtual.apply_row(row)

    def _sort_args(self, args, kwargs):
        query = {}
        fetch = '*'
        if args:
            query = args[0]
            fetch = args[1] if len(args) > 1 else '*'
        if kwargs:
            fetch = kwargs['fetch'] if 'fetch' in kwargs else '*'
            kwargs.pop('fetch', None)
            query = args[0] if args else kwargs or {}

        return query, fetch

    def populate(self, *args, **kwargs):
        query, fetch = self._sort_args(args, kwargs)

        result = self.find_one(query=query, fetch=fetch)
        for result_item in result:
            if result_item in self._expand_param:
                setattr(
                    self, result_item, self.find_one({
                            result_item: result[result_item]
                        }, self._expand_param[result_item]
                    )
                )
            else:
                setattr(self, result_item, result[result_item])

    def populate_many(self, *args, **kwargs):
        query, fetch = self._sort_args(args, kwargs)

        result = self.find(query=query, fetch=fetch)
        all_columns = []
        for col in result[0]:  # Re declaration of col due to the fetch potentially not holding all columns.
            all_columns.append(col)
        for col in all_columns:
            temp = []
            for result_item in result:
                temp.append(result_item[col])
            setattr(self, col, temp)
        # Populate many assigns a list of all results to the attribute, instead of a single value.

    def save(self):
        if not getattr(self, 'ID'):
            raise Exception('No ID')
        query = {'ID': getattr(self, 'ID')}
        update = {}
        for column in self._attrs:
            if getattr(self, column):
                update[column] = getattr(self, column)
        print(query)
        print(update)
        self.find_and_update(query=query, update=update)

    def update(self, *args, **kwargs):
        update = args[0] if args else kwargs or {}
        if not getattr(self, 'ID'):
            raise Exception('No ID')
        query = {'ID': getattr(self, 'ID')}
        for r_update in update:
            setattr(self, r_update, update[r_update])
        self.find_and_update(query=query, update=update)

    def __str__(self):
        string = {}
        for col in self._attrs:
            string[col] = getattr(self, col)
        return str(string)

    def __repr__(self):
        string = {}
        for col in self._attrs:
            string[col] = getattr(self, col)
        return str(string)


class LiteSchema(SqLiteModel):
    def __init__(self, db_credentials, table, f_keys=None):
        super().__init__(db_credentials, table, f_keys)
        self._parameters = {}
        self._attrs = []
        self._virtual = None
        self.virtual = Virtual()
        self._expand_param = {}

    def init_schema(self, method, params):
        if len(method) != 0:
            create = getattr(self, method[0])(params)
            self.populate({'ID': create['ID']})

    def add_param(self, name, options=None):
        if options is None:
            options = {}
        self._parameters[name] = options

    def add_params(self, names):
        columns = self._columns()
        names['ID'] = {}
        setattr(self, 'createdAt', None)
        setattr(self, 'updatedAt', None)
        self._attrs.append('createdAt')
        self._attrs.append('updatedAt')
        for option in names:
            setattr(self, option, None)
            self._attrs.append(option)
            if option not in columns:
                self._create_column(
                    col_name=option, options=names[option]
                ) if 'dbtype' not in names[option] else self._create_column(
                    col_name=option, col_type=names[option]['dbtype'], options=names[option]
                )
            self._parameters[option] = names[option]
            for item in names[option]:
                if 'required' in item:
                    self._required.append(option)

    def expand_param(self, *args, **kwargs):
        kwargs['fetch'] = '*' if 'fetch' not in kwargs else kwargs['fetch']
        self._expand_param[kwargs['param']] = kwargs['fetch']

    def add_virtual(self, virtual):
        self._virtual = virtual

    def populate_virtual(self):
        query = {
            self._virtual['foreign_column']: getattr(self, self._virtual['field'])
        }

        result = self.find(query=query, table=self._virtual['table'])

        for row in result:
            self.virtual.apply_row(row)

    def _sort_args(self, args, kwargs):
        query = {}
        fetch = '*'
        if args:
            query = args[0]
            fetch = args[1] if len(args) > 1 else '*'
        if kwargs:
            fetch = kwargs['fetch'] if 'fetch' in kwargs else '*'
            kwargs.pop('fetch', None)
            query = args[0] if args else kwargs or {}

        return query, fetch

    def populate(self, *args, **kwargs):
        query, fetch = self._sort_args(args, kwargs)

        result = self.find_one(query=query, fetch=fetch)
        for result_item in result:
            if result_item in self._expand_param:
                setattr(
                    self, result_item, self.find_one({
                            result_item: result[result_item]
                        }, self._expand_param[result_item]
                    )
                )
            else:
                setattr(self, result_item, result[result_item])

    def populate_many(self, *args, **kwargs):
        query, fetch = self._sort_args(args, kwargs)

        result = self.find(query=query, fetch=fetch)
        all_columns = []
        for col in result[0]:  # Re declaration of col due to the fetch potentially not holding all columns.
            all_columns.append(col)
        for col in all_columns:
            temp = []
            for result_item in result:
                temp.append(result_item[col])
            setattr(self, col, temp)
        # Populate many assigns a list of all results to the attribute, instead of a single value.

    def save(self):
        if not getattr(self, 'ID'):
            raise Exception('No ID')
        query = {'ID': getattr(self, 'ID')}
        update = {}
        for column in self._attrs:
            if getattr(self, column):
                update[column] = getattr(self, column)

        self.find_and_update(query=query, update=update)

    def update(self, *args, **kwargs):
        update = args[0] if args else kwargs or {}
        if not getattr(self, 'ID'):
            raise Exception('No ID')
        query = {'ID': getattr(self, 'ID')}
        for r_update in update:
            setattr(self, r_update, update[r_update])
        self.find_and_update(query=query, update=update)

    def __str__(self):
        string = {}
        for col in self._attrs:
            string[col] = getattr(self, col)
        return str(string)

    def __repr__(self):
        string = {}
        for col in self._attrs:
            string[col] = getattr(self, col)
        return str(string)

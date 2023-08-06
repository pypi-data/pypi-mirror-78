#  Vys Documentation


## DB Schema documentation:

### SqLite Syntax
```python
from Vys import models

cfg = models.DbCredentials(database='test.db')

class Employee(models.LiteSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(db_credentials=cfg, table='employee')
```

### Create the schema parameters
```python
class Employee(models.LiteSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(db_credentials=cfg, table='employee')
        self.add_params({
            'name': {
                'dbtype': 'varchar(255)',
                'type': str
            },
            'manager': {
                'dbtype': 'varchar(9)'
            }
        })
        self.init_schema(args, kwargs)
```
IDs for SqLite are added automatically. 

Dbtype and type is different purely for validation purposes - type is for schema validation, dbtype corresponds to the data type in the database. 

### Query
```python
user = User
x = user.find(
    query={
        'user': 'connor.white'
    },
    fetch=['perms']
)
# Returns [{'ID': 'ShlLuRWaa', 'createdAt': '2020-09-04 11:32:44.132863', 'updatedAt': '2020-09-04 11:32:44.132863', 'manager': None, 'name': 'tefrstf'}

x = user.find_one(
    query={
        'user': 'connor.white'
    },
    fetch=['perms']
)
# Returns {'ID': 'ShlLuRWaa', 'createdAt': '2020-09-04 11:32:44.132863', 'updatedAt': '2020-09-04 11:32:44.132863', 'manager': None, 'name': 'tefrstf'}

user.populate(
    query={'name': 'tefrstf'} 
)
print(user)

# OR

user.populate(
    name='newname'
)

# Returns # Returns {'ID': 'ShlLuRWaa', 'createdAt': '2020-09-04 11:32:44.132863', 'updatedAt': '2020-09-04 11:32:44.132863', 'manager': None, 'name': 'tefrstf'}

user.populate_many(
    query={'name': 'tefrstf'} 
)
print(user)
# Returns {'createdAt': ['2020-09-04 11:32:44.132863', '2020-09-04 11:33:02.841748', '2020-09-04 11:33:37.348974', '2020-09-04 11:37:57.689165', '2020-09-04 11:38:11.541987', '2020-09-04 11:39:46.465859', '2020-09-04 11:40:28.353423'], 'updatedAt': ['2020-09-04 11:32:44.132863', '2020-09-04 11:33:02.841748', '2020-09-04 11:33:37.348974', '2020-09-04 11:37:57.689165', '2020-09-04 11:38:11.541987', '2020-09-04 11:39:46.465859', '2020-09-04 11:40:28.353423'], 'name': ['tefrstf', 'tefrstf', 'tefrstf', 'tefrstf', 'tefrstf', 'tefrstf', 'tefrstf'], 'manager': [None, None, None, None, None, None, None], 'ID': ['ShlLuRWaa', 'jkkVrB06P', 'LXCBlqUhN', 'tLCrf5EzW', '8EJzjBtwO', 'TrPxwtTXo', 'wRTuXYKe1']}

```
The fetch parameter is not required here, excluding it will return all columns. Find will return multiple, find_one only one. 

### Create
```python
User.create({
    'user': 'new',
    'password': 'hffgv'
})

user = User('create', name='name', password='hffgv')

```
The id will be done automatically, as will the "CreatedAt" and "UpdatedAt" Fields. This will insert a new row into the db. 

### Update
```python
User.find_and_update(
    query={
        'perms': 'user'
    },
    update={
        'perms': 'silly'
    }
)

############################################

User.populate({
    'name': 'tefrstf'
})

mark.update({
    'name': 'testing123'
})

# OR

mark.update(
    name='testing123'
)
```
Find and update will update all instances - as the "find" function returns a python dict, you can input them directly into the query section here.
Using the .update function on a class that has been populated will only update that row.

### Adding a foreign key to a table. 

```python
options = {
    'column': 'manager',
    'table': 'managers',
    'foreign column': 'ID'
}


class Employee(models.LiteSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(db_credentials=cfg, table='employee', f_keys=options)
        self.add_params({
            'name': {
                'dbtype': 'varchar(255)',
                'type': str
            },
            'manager': {
                'dbtype': 'varchar(9)'
            }
        })
        self.expand_param(
            param='manager',
            fetch='ID, name'
        )
        self.init_schema(args, kwargs)


```
This snippet creates a column linked to a foreign key. In the "options" dict, the keys should be self explanatory.
The expand_param function expands the return - so instead of returning the ID of the field, it will return info from the column in which that key is present in the other table. 

### Creating the virtual population. 
```python
class Manager(models.LiteSchema):
    def __init__(self, db_credentials=cfg, table='managers'):
        super().__init__(db_credentials, table)
        self.add_params({
            'name': {
                'dbtype': 'varchar(255)',
                'type': str
            }
        })
        self.add_virtual({
            'table': 'employee',
            'foreign_column': 'manager',
            'field': 'ID'
        })

```
The dict takes 3 arguments. "Table" is the target table where the foreign key is located. "Foreign column" is the column where the key is located. "Field" is the local column where the key is located. 

### Populating the virtual field.
```python
manager = Manager()

manager.populate_new(name='connor')
manager.populate_virtual()

print(manager.virtual)

# Returns [{'ID': 'o0l5i2nIr', 'createdAt': '2020-08-31 20:51:08.422624', 'updatedAt': '2020-09-02 08:43:51.600846', 'manager': 'w47mlx4df', 'name': 'mark'}]

print(manager.virtual.o0l5i2nIr)

# Returns {'ID': 'o0l5i2nIr', 'createdAt': '2020-08-31 20:51:08.422624', 'updatedAt': '2020-09-02 08:43:51.600846', 'manager': 'w47mlx4df', 'name': 'mark'}

```





## Datetime manipulation

### DatetimeGenerator
```python
datetime_object = DatetimeGenerator(
    datetime_input=datetime.strptime('2000-08-31 10:22:08', '%Y-%m-%d %H:%M:%S'),
    format='iso',
    str_format='%Y-%m-%d'
)
datetime_object.add(hours=9, days=12)
```
Datetime input can be any datetime object.
Format can be either "datetime", "iso", "unix", or "string".

Leaving datetime input blank will generate the current time. Leaving the format blank defaults to datetime. Str_format 
should only be used when the format is put as string. 

You can add or subtract values of time with the add and subtract methods. 


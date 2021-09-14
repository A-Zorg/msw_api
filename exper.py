import configparser
import paramiko
from base.sql_request import dr
from base.tools.dr_fun import previous_business_day, get_time_param
import os
import numpy

from base.sql_functions import pgsql_select, pgsql_select_as_dict, \
    pgsql_update, pgsql_insert, pgsql_del

config = configparser.ConfigParser()
config.read("cred/config.ini")

def download_from_server(file_name):
    """download"""
    host = config["server"]["host"]
    port = config["server"]["port"]
    username = config["server"]["username"]
    password = config["server"]["password"]

    with paramiko.Transport((host, int(port))) as transport:
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remotepath = f'/smartteam/msw_server_9999/msw/msw/{file_name}'
        localpath = f'C:\\Users\\wsu\\Desktop\\{file_name}'
        sftp.get(remotepath, localpath)

        sftp.close()

# download_from_server('settings.py')
import datetime
# now = datetime.datetime.now()
# print(now.strftime('%B %d, %Y, %I:%M %p'))
# asd = 'July 1, 2021, 6:55 a.m.'
# print(datetime.datetime.strptime(asd.replace('.', ''), '%B %d, %Y, %I:%M %p'))
#
# df = '01 Jul 2021 08:59:54.109000'
# print(datetime.datetime.strptime(df, '%d %b %Y %H:%M:%S.%f'))
# r''

print(datetime.datetime.strptime('July', '%B').month)

a = 5
asd = {}
b = asd.get('f')

print(b)

print(15<<1)

import sys
a='aasdagfgsdfgsdfklsdjfhlskdfjhoi54uh945u945uhw95uh09weu5h0w495hhsdfhsdfh'
print('asd')
print(sys.getrefcount(a))

fgt = [1,2,3,4,5]
fgt[::-1][1]=3
print(fgt)





class FieldParameters():
    oooo = 1234
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            # print(type(key))
            setattr(self, key, value)

single_date = datetime.date(2021, 4, 12)
effective_date = datetime.datetime.combine(single_date,
                                                   datetime.time(hour=23, minute=59, second=0, microsecond=0))
print(effective_date+datetime.timedelta(milliseconds=1))


# class X:
#     def asd(self):
#         print(123)
#     def gh(self):
#         print(7897)

# class UserBillTypes(X):
#     asdas = 80
# a =UserBillTypes()

# print(a)

# class GeneralFieldf
import re
from datetime import datetime, date, time


class GeneralField():
    def __init__(self, is_encoded, blank):
        self.is_encoded = is_encoded
        self.blank = blank

class TextField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = str
        self.sql_formate = 'text'

class IntField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = int
        self.sql_formate = 'int'

class FloatField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = float
        self.sql_formate = 'float'

class DateField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = date

class DateTimeField(GeneralField):
    def __init__(self, is_encoded=False, blank=False, auto_fill=False):
        super().__init__(is_encoded, blank)
        self.obj_type = datetime
        self.auto_fill = auto_fill

class TimeField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = time

class ForeignKeyField(GeneralField):
    def __init__(self, table_cls, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = table_cls
        self.sql_formate = 'int'


# def get_attrs(cls):
#     fields = {}
#     for field in dir(cls):
#         if field[-4:] == '_atr':
#             fields[field[:-4]] = getattr(cls, field)
#     return fields
#
# sign_codes = {
#     'in': ' in ({}),',
#     'gt': ' > {},',
#     'gte': ' >= {},',
#     'lt': ' < {},',
#     'lte': ' <= {},',
#     'like': ' like {},',
# }
#
# def parse_field(field_name):
#     try:
#         particles = field_name.split('__')
#         for key, value in sign_codes.items():
#             if key == particles[1]:
#                 if len(particles) > 2:
#                     return particles[0], particles[0] + value, particles[2]
#                 else:
#                     return particles[0], particles[0] + value, None
#         else:
#             return particles[0], particles[0] + ' = {},', particles[1]
#     except:
#         return field_name, field_name + ' = {},', None
#
# def formate_value(field_type, value):
#     if field_type.obj_type == str:
#         return f"'{value}'"
#     elif field_type.obj_type == int:
#         return int(value)
#     elif field_type.obj_type == float:
#         return float(value)
#     elif field_type.obj_type == datetime:
#         first_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}', value)
#         second_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value)
#         if first_var or second_var:
#             return f"timestamp'{value}'"
#         else:
#             raise Exception(f"{value} is not correct date(ex. yyyy-mm-dd ) "
#                             f"or datetime (ex. yyyy-mm-dd hh:mm:ss)")
#     elif field_type.obj_type == date:
#         if re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value):
#             return f"date'{value}'"
#         else:
#             raise Exception(f"{value} is not date (ex. yyyy-mm-dd )")
#     elif field_type.obj_type == time:
#         if re.findall('^[\d]{2}:[\d]{2}:[\d]{2}', value):
#             return f"time'{value}'"
#         else:
#             raise Exception(f"{value} is not time (ex. hh:mm:ss )")
#     else:
#         try:
#             return value.id
#         except:
#             return value
#
# def decrypting_or_not(field_type, field_name, parsed_field):
#     if field_type.is_encoded:
#         return parsed_field.replace(
#             field_name,
#             f"pgp_sym_decrypt({field_name}::bytea, "
#             f"'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6')::{field_type.sql_formate}"
#         )
#     else:
#         return parsed_field
#
# def encrypting_or_not(field_type, parsed_field):
#     if field_type.is_encoded:
#         return parsed_field.format(
#             "pgp_sym_encrypt({}, 'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6', 'cipher-algo=aes256')"
#         )
#     else:
#         return parsed_field
#
# def get_if_foreign_object(field_type, foreign_field, value):
#     gotten_object = field_type.obj_type.get(**{foreign_field:value})
#     return gotten_object.id
#
# def check_creating_list(fields, values):
#     given_keys = values.keys()
#     for field_name, field_type in fields.items():
#         if hasattr(field_type, "auto_fill") and field_type.auto_fill and field_name not in given_keys:
#             values[field_name] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         elif not field_type.blank and field_name not in given_keys:
#             raise Exception(f"{field_name} was missed")
#     return values
#
#
#
# def get_search_part(fields, values):
#     search_part = 'WHERE '
#     for field_name, value in values.items():
#         field_name, parsed_field, foreign_field = parse_field(field_name)
#         field_type = fields[field_name]
#         parsed_field = decrypting_or_not(field_type, field_name, parsed_field)
#         if 'in ({})' in parsed_field:
#             values_set = set()
#             for part in value:
#                 formated_part = formate_value(field_type, part)
#                 values_set.add(formated_part)
#             search_part += parsed_field.format(str(values_set)[1:-1])
#         else:
#             if foreign_field:
#                 value = get_if_foreign_object(field_type, foreign_field, value)
#             formated_value = formate_value(field_type, value)
#             search_part += parsed_field.format(formated_value)
#     else:
#         search_part = search_part[:-1]
#     return search_part
#
# def get_search_id_part(fields, values):
#     return f' WHERE id = {values.id}'
#
# def get_set_part(fields, values):
#     search_part = 'SET '
#     for field_name, field_type in fields.items():
#         field_name, parsed_field, _ = parse_field(field_name)
#         value = getattr(values, field_name)
#
#         parsed_field = encrypting_or_not(field_type, parsed_field)
#         formated_value = formate_value(field_type, value)
#
#         search_part += parsed_field.format(formated_value)
#     else:
#         search_part = search_part[:-1]
#
#     return search_part
#
# def get_values_part(fields, values):
#     search_part = 'VALUES ('
#     for field_name, field_value in values.items():
#         field_type = fields[field_name]
#         parsed_field = '{},'
#
#         parsed_field = encrypting_or_not(field_type, parsed_field)
#         formated_value = formate_value(field_type, field_value)
#
#         search_part += parsed_field.format(formated_value)
#     else:
#         search_part = search_part[:-1]
#         search_part += ')'
#
#     return search_part
#
# def get_select_part(fields):
#     select_part = 'SELECT '
#     for field_name, field in fields.items():
#         select_part += field_name + ', '
#         select_part = decrypting_or_not(field, field_name, select_part)
#     else:
#         select_part = select_part[:-2]
#
#     return select_part
#
# def get_from_part(cls):
#     return f' FROM {cls.table_name} '
#
# def get_update_part(cls):
#     return f'UPDATE {cls.table_name} '
#
# def get_insert_part(cls, values):
#     fields = ', '.join(values.keys())
#     return f'INSERT INTO {cls.table_name} ({fields}) '
#
# def parse_sql_response(sql_response, cls):
#     objects_list = []
#     for row in sql_response:
#         new_object = cls()
#         for key, value in row.items():
#             setattr(new_object, key, value)
#         objects_list.append(new_object)
#     return objects_list



class Model:

    sign_codes = {
        'in': ' in ({}),',
        'gt': ' > {},',
        'gte': ' >= {},',
        'lt': ' < {},',
        'lte': ' <= {},',
        'like': ' like {},',
    }

    @classmethod
    def get_attrs(cls):
        fields = {}
        for field in dir(cls):
            if field[-4:] == '_atr':
                fields[field[:-4]] = getattr(cls, field)
        return fields

    @classmethod
    def _parse_field(cls, field_name):
        try:
            particles = field_name.split('__')
            for key, value in cls.sign_codes.items():
                if key == particles[1]:
                    if len(particles) > 2:
                        return particles[0], particles[0] + value, particles[2]
                    else:
                        return particles[0], particles[0] + value, None
            else:
                return particles[0], particles[0] + ' = {},', particles[1]
        except:
            return field_name, field_name + ' = {},', None

    @classmethod
    def formate_value(cls, field_type, value):
        if field_type.obj_type == str:
            return f"'{value}'"
        elif field_type.obj_type == int:
            return int(value)
        elif field_type.obj_type == float:
            return float(value)
        elif field_type.obj_type == datetime:
            first_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}', value)
            second_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value)
            if first_var or second_var:
                return f"timestamp'{value}'"
            else:
                raise Exception(f"{value} is not correct date(ex. yyyy-mm-dd ) "
                                f"or datetime (ex. yyyy-mm-dd hh:mm:ss)")
        elif field_type.obj_type == date:
            if re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value):
                return f"date'{value}'"
            else:
                raise Exception(f"{value} is not date (ex. yyyy-mm-dd )")
        elif field_type.obj_type == time:
            if re.findall('^[\d]{2}:[\d]{2}:[\d]{2}', value):
                return f"time'{value}'"
            else:
                raise Exception(f"{value} is not time (ex. hh:mm:ss )")
        else:
            try:
                return value.id
            except:
                return value

    @classmethod
    def decrypting_or_not(cls, field_type, field_name, parsed_field):
        if field_type.is_encoded:
            return parsed_field.replace(
                field_name,
                f"pgp_sym_decrypt({field_name}::bytea, "
                f"'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6')::{field_type.sql_formate}"
            )
        else:
            return parsed_field

    @classmethod
    def encrypting_or_not(cls, field_type, parsed_field):
        if field_type.is_encoded:
            return parsed_field.format(
                "pgp_sym_encrypt({}, 'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6', 'cipher-algo=aes256')"
            )
        else:
            return parsed_field

    @classmethod
    def get_if_foreign_object(cls, field_type, foreign_field, value):
        gotten_object = field_type.obj_type.get(**{foreign_field:value})
        return gotten_object.id

    @classmethod
    def check_creating_list(cls, fields, values):
        given_keys = values.keys()
        for field_name, field_type in fields.items():
            if hasattr(field_type, "auto_fill") and field_type.auto_fill and field_name not in given_keys:
                values[field_name] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elif not field_type.blank and field_name not in given_keys:
                raise Exception(f"{field_name} was missed")
        return values


    @classmethod
    def get_search_part(cls, fields, values):
        search_part = 'WHERE '
        for field_name, value in values.items():
            field_name, parsed_field, foreign_field = cls._parse_field(field_name)
            field_type = fields[field_name]
            parsed_field = cls.decrypting_or_not(field_type, field_name, parsed_field)
            if 'in ({})' in parsed_field:
                values_set = set()
                for part in value:
                    formated_part = cls.formate_value(field_type, part)
                    values_set.add(formated_part)
                search_part += parsed_field.format(str(values_set)[1:-1])
            else:
                if foreign_field:
                    value = cls.get_if_foreign_object(field_type, foreign_field, value)
                formated_value = cls.formate_value(field_type, value)
                search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]
        return search_part

    @classmethod
    def get_search_id_part(cls, fields, values):
        return f' WHERE id = {values.id}'

    @classmethod
    def get_set_part(cls, fields, values):
        search_part = 'SET '
        for field_name, field_type in fields.items():
            field_name, parsed_field, _ = cls._parse_field(field_name)
            value = getattr(values, field_name)

            parsed_field = cls.encrypting_or_not(field_type, parsed_field)
            formated_value = cls.formate_value(field_type, value)

            search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]

        return search_part

    @classmethod
    def get_values_part(cls, fields, values):
        search_part = 'VALUES ('
        for field_name, field_value in values.items():
            field_type = fields[field_name]
            parsed_field = '{},'

            parsed_field = cls.encrypting_or_not(field_type, parsed_field)
            formated_value = cls.formate_value(field_type, field_value)

            search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]
            search_part += ')'

        return search_part

    @classmethod
    def get_select_part(cls, fields):
        select_part = 'SELECT '
        for field_name, field in fields.items():
            select_part += field_name + ', '
            select_part = cls.decrypting_or_not(field, field_name, select_part)
        else:
            select_part = select_part[:-2]

        return select_part

    @classmethod
    def get_from_part(cls):
        return f' FROM {cls.table_name} '

    @classmethod
    def get_update_part(cls):
        return f'UPDATE {cls.table_name} '

    @classmethod
    def get_insert_part(cls, values):
        fields = ', '.join(values.keys())
        return f'INSERT INTO {cls.table_name} ({fields}) '

    @classmethod
    def parse_sql_response(cls, sql_response):
        objects_list = []
        for row in sql_response:
            new_object = cls()
            for key, value in row.items():
                setattr(new_object, key, value)
            objects_list.append(new_object)
        return objects_list

    @classmethod
    def _search_request(cls, search_fields):
        fields = cls.get_attrs()
        request = cls.get_select_part(fields) \
                  + cls.get_from_part() \
                  + cls.get_search_part(fields, search_fields)

        return cls.parse_sql_response(pgsql_select_as_dict(request, **config['pg_db_9999']))

    def _update_request(self, cls):
        fields = cls.get_attrs()
        request = cls.get_update_part(cls) \
                  + cls.get_set_part(fields, self) \
                  + cls.get_search_id_part(fields, self)

        return pgsql_update(request, **config['pg_db_9999'])

    @classmethod
    def _insert_request(cls, given_values):
        fields = cls.get_attrs()
        given_values = cls.check_creating_list(fields, given_values)
        request = cls.get_insert_part(given_values) \
                  + cls.get_values_part(fields, given_values) \

        return pgsql_insert(request, **config['pg_db_9999'])


    @classmethod
    def create(cls, **kwargs):
        return cls._insert_request(kwargs)

    def save(self):
        cls = self.__class__
        return self._update_request(cls)

    @classmethod
    def get(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) > 1:
            raise Exception(f"get more then 1 objects {cls}")
        elif len(objects_list) == 0:
            raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list[0]

    @classmethod
    def filter(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) == 0:
            raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list



class Broker(Model):
    table_name = 'accounting_system_broker'
    id_atr = IntField(blank=True)
    name_atr = TextField()

#     def _search_request(cls, search_fields):
#         fields = get_attrs(cls)
#         request = get_select_part(fields) \
#                   + get_from_part(cls) \
#                   + get_search_part(fields, search_fields)
#
#         return parse_sql_response(pgsql_select_as_dict(request, **config['pg_db_9999']), cls)
#
#     def _update_request(cls, self):
#         fields = get_attrs(cls)
#         request = get_update_part(cls) \
#                   + get_set_part(fields, self) \
#                   + get_search_id_part(fields, self)
#
#         return pgsql_update(request, **config['pg_db_9999'])
#
#     def _insert_request(cls, given_values):
#         fields = get_attrs(cls)
#         given_values = check_creating_list(fields, given_values)
#         request = get_insert_part(cls, given_values) \
#                   + get_values_part(fields, given_values) \
#
#         return pgsql_insert(request, **config['pg_db_9999'])
#
#     @classmethod
#     def create(cls, **kwargs):
#         return cls._insert_request(cls, kwargs)
#
#     def save(self):
#         cls = self.__class__
#         return cls._update_request(cls, self)
#
#     @classmethod
#     def get(cls, **kwargs):
#         objects_list = cls._search_request(cls, kwargs)
#
#         if len(objects_list) > 1:
#             raise Exception(f"get more then 1 objects {cls}")
#         elif len(objects_list) == 0:
#             raise Exception(f"there is no object with parameters:{kwargs} {cls}")
#         else:
#             return objects_list[0]
#
#     @classmethod
#     def filter(cls, **kwargs):
#         objects_list = cls._search_request(cls, kwargs)
#
#         if len(objects_list) == 0:
#             raise Exception(f"there is no object with parameters:{kwargs} {cls}")
#         else:
#             return objects_list
#
#
# class AccountType():
#     table_name = 'accounting_system_accounttype'
#     id_atr = IntField(blank=True)
#     account_regexp_atr = TextField()
#     broker_id_atr = ForeignKeyField(Broker)
#
#     def _search_request(cls, search_fields):
#         fields = get_attrs(cls)
#         request = get_select_part(fields) \
#                   + get_from_part(cls) \
#                   + get_search_part(fields, search_fields)
#         return parse_sql_response(pgsql_select_as_dict(request, **config['pg_db_9999']), cls)
#
#     @classmethod
#     def get(cls, **kwargs):
#         fields = get_attrs(cls)
#         request = get_select_part(fields) \
#                   + get_from_part(cls) \
#                   + get_search_part(fields, kwargs)
#         print(request)


# print(Broker.get(name='Takion').name)
# AccountType.get(broker_id__id=2)

# a =Broker()
# a.update_request()
# asd = Broker.get(name="Takion")
# asd.name = 'Takion'
# print(asd.save())

# print(Broker.create(name='Bofop'))

class MassModel(list):
    def delete(self):
        id_list = [obj_mod.id for obj_mod in self]
        return self[0]._Model1__mass_delete(id__in=id_list)

    def sorted_by(self, *args, desc=False):
        sort_func = lambda x: [getattr(x, arg) for arg in args]
        sorted(self, key=sort_func, reverse=desc)



class Model1:
    @classmethod
    def get_attrs(cls):
        fields = {}
        for field in dir(cls):
            if field[-4:] == '_atr':
                fields[field[:-4]] = getattr(cls, field)
        return fields

    @staticmethod
    def parse_field(field_name):
        sign_codes = {
            'in': ' in ({}),',
            'gt': ' > {},',
            'gte': ' >= {},',
            'lt': ' < {},',
            'lte': ' <= {},',
            'like': ' like {},',
        }
        try:
            particles = field_name.split('__')
            for key, value in sign_codes.items():
                if key == particles[1]:
                    if len(particles) > 2:
                        return particles[0], particles[0] + value, particles[2]
                    else:
                        return particles[0], particles[0] + value, None
            else:
                return particles[0], particles[0] + ' = {},', particles[1]
        except:
            return field_name, field_name + ' = {},', None

    @staticmethod
    def formate_value(field_type, value):
        if field_type.obj_type == str:
            return f"'{value}'"
        elif field_type.obj_type == int:
            return int(value)
        elif field_type.obj_type == float:
            return float(value)
        elif field_type.obj_type == datetime:
            first_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}', value)
            second_var = re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value)
            if first_var or second_var:
                return f"timestamp'{value}'"
            else:
                raise Exception(f"{value} is not correct date(ex. yyyy-mm-dd ) "
                                f"or datetime (ex. yyyy-mm-dd hh:mm:ss)")
        elif field_type.obj_type == date:
            if re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value):
                return f"date'{value}'"
            else:
                raise Exception(f"{value} is not date (ex. yyyy-mm-dd )")
        elif field_type.obj_type == time:
            if re.findall('^[\d]{2}:[\d]{2}:[\d]{2}', value):
                return f"time'{value}'"
            else:
                raise Exception(f"{value} is not time (ex. hh:mm:ss )")
        else:
            try:
                return value.id
            except:
                return value

    @staticmethod
    def decrypting_or_not(field_type, field_name, parsed_field):
        if field_type.is_encoded:
            return parsed_field.replace(
                field_name,
                f"pgp_sym_decrypt({field_name}::bytea, "
                f"'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6')::{field_type.sql_formate}"
            )
        else:
            return parsed_field

    @staticmethod
    def encrypting_or_not(field_type, parsed_field):
        if field_type.is_encoded:
            return parsed_field.format(
                "pgp_sym_encrypt({}, 'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6', 'cipher-algo=aes256')"
            )
        else:
            return parsed_field

    @staticmethod
    def get_if_foreign_object(field_type, foreign_field, value):
        gotten_object = field_type.obj_type.get(**{foreign_field:value})
        return gotten_object.id

    @staticmethod
    def check_creating_list(fields, values):
        given_keys = values.keys()
        for field_name, field_type in fields.items():
            if hasattr(field_type, "auto_fill") and field_type.auto_fill and field_name not in given_keys:
                values[field_name] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elif not field_type.blank and field_name not in given_keys:
                raise Exception(f"{field_name} was missed")
        return values

    @classmethod
    def get_search_part(cls, fields, values):
        search_part = 'WHERE '
        for field_name, value in values.items():
            field_name, parsed_field, foreign_field = cls.parse_field(field_name)
            field_type = fields[field_name]
            parsed_field = cls.decrypting_or_not(field_type, field_name, parsed_field)
            if 'in ({})' in parsed_field:
                values_set = set()
                for part in value:
                    formated_part = cls.formate_value(field_type, part)
                    values_set.add(formated_part)
                search_part += parsed_field.format(str(values_set)[1:-1])
            else:
                if foreign_field:
                    value = cls.get_if_foreign_object(field_type, foreign_field, value)
                formated_value = cls.formate_value(field_type, value)
                search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]
        return search_part

    def get_search_id_part(self):
        return f' WHERE id = {self.id}'

    def get_set_part(self, fields):
        search_part = 'SET '
        for field_name, field_type in fields.items():
            field_name, parsed_field, _ = self.parse_field(field_name)
            value = getattr(self, field_name)

            parsed_field = self.encrypting_or_not(field_type, parsed_field)
            formated_value = self.formate_value(field_type, value)

            search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]

        return search_part

    @classmethod
    def get_values_part(cls, fields, values):
        search_part = '('
        for field_name, field_value in values.items():
            field_type = fields[field_name]
            parsed_field = '{},'

            parsed_field = cls.encrypting_or_not(field_type, parsed_field)
            formated_value = cls.formate_value(field_type, field_value)

            search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-1]
            search_part += ')'

        return search_part

    @classmethod
    def get_select_part(cls, fields):
        select_part = 'SELECT '
        for field_name, field in fields.items():
            select_part += field_name + ', '
            select_part = cls.decrypting_or_not(field, field_name, select_part)
        else:
            select_part = select_part[:-2]

        return select_part

    @classmethod
    def get_select_all_part(cls):
        return 'SELECT * '

    @classmethod
    def get_from_part(cls):
        return f' FROM {cls.table_name} '

    @classmethod
    def get_update_part(cls):
        return f'UPDATE {cls.table_name} '

    @classmethod
    def get_insert_part(cls, values):
        fields = ', '.join(values.keys())
        return f'INSERT INTO {cls.table_name} ({fields}) '

    @classmethod
    def parse_sql_response(cls, sql_response):
        objects_list = MassModel()
        for row in sql_response:
            new_object = cls()
            for key, value in row.items():
                setattr(new_object, key, value)
            objects_list.append(new_object)
        return objects_list

    @classmethod
    def _search_request(cls, search_fields):
        fields = cls.get_attrs()
        request = \
            cls.get_select_part(fields) \
            + cls.get_from_part() \
            + cls.get_search_part(fields, search_fields)

        return cls.parse_sql_response(pgsql_select_as_dict(request, **config['pg_db_9999']))

    @classmethod
    def _search_all_request(cls):
        request = \
            cls.get_select_all_part() \
            + cls.get_from_part()

        return cls.parse_sql_response(pgsql_select_as_dict(request, **config['pg_db_9999']))

    def _update_request(self, cls):
        fields = cls.get_attrs()
        request = \
            self.get_update_part() \
            + self.get_set_part(fields) \
            + self.get_search_id_part()

        return pgsql_update(request, **config['pg_db_9999'])

    def _delete_request(self, cls):
        request = \
            'DELETE ' \
            + self.get_from_part() \
            + self.get_search_id_part()
        print(request)
        return pgsql_del(request, **config['pg_db_9999'])

    @classmethod
    def _insert_request(cls, given_values):
        fields = cls.get_attrs()
        given_values = cls.check_creating_list(fields, given_values)
        request = \
            cls.get_insert_part(given_values) + \
            'VALUES ' + \
            cls.get_values_part(fields, given_values)
        pgsql_insert(request, **config['pg_db_9999'])

        return cls.get(**given_values)

    @classmethod
    def bulk_insert_request(cls, given_rows):
        fields = cls.get_attrs()

        for row in given_rows:
            cls.check_creating_list(fields, row)
        fields_list = given_rows[0]

        request = \
            cls.get_insert_part(fields_list) + \
            'VALUES '

        for row in given_rows:
            request += (cls.get_values_part(fields, row) + ',')
        else:
            request = request[:-1]
        pgsql_insert(request, **config['pg_db_9999'])

        return MassModel([cls.get(**row) for row in given_rows])

    @classmethod
    def __mass_delete(cls, **kwargs):
        fields = cls.get_attrs()
        request = \
            'DELETE ' \
            + cls.get_from_part() \
            + cls.get_search_part(fields, kwargs)
        return pgsql_del(request, **config['pg_db_9999'])

    @classmethod
    def bulk_create(cls, **kwargs):
        return cls.bulk_insert_request(kwargs)

    @classmethod
    def create(cls, **kwargs):
        return cls._insert_request(kwargs)

    def save(self):
        cls = self.__class__
        return self._update_request(cls)

    def delete(self):
        cls = self.__class__
        return self._delete_request(cls)

    @classmethod
    def get(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) > 1:
            raise Exception(f"get more then 1 objects {cls}")
        elif len(objects_list) == 0:
            raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list[0]

    @classmethod
    def filter(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) == 0:
            raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list

    @classmethod
    def all(cls):
        objects_list = cls._search_all_request()

        if len(objects_list) == 0:
            raise Exception(f"there is no object {cls}")
        else:
            return objects_list

class Broker1(Model1):
    table_name = 'accounting_system_broker'
    id_atr = IntField(blank=True)
    name_atr = TextField()



# print(Broker.get(name='Takion').name)
# AccountType.get(broker_id__id=2)

# a =Broker()
# a.update_request()
# asd = Broker1.get(name="Lakion")
# print(asd.delete())
# asd.name = 'Lakion'
# print(asd.save())
# rty = Broker1.filter(id__gt=3)
# print(rty[0].name)
# asd = Broker1.bulk_insert_request([
#     {'name': 'asdasd'},
#     {'name': 'sdfsdfsd'}
# ])
# asd = Broker1.create(name='Bofop')
# print(asd[1].id)
# print(asd.id)
# print(asd.name)
# print(Broker1.filter(id__gte=7).delete())
# a = Broker1()
# print(a._Model1__mass_delete(id__in=[1,2,3,4]))
# print(getattr(a, '_Model1__mass_delete'))
# #
# asd = [{'date': '2021-02-28T23:59:59.999999', 'amount': 0, 'changes': 0}, {'date': '2021-03-31T23:59:59.999999', 'amount': -2.5, 'changes': -2.5}, {'date': '2021-04-30T23:59:59.999999', 'amount': -144.6, 'changes': -142.1}, {'date': '2021-05-17', 'amount': -132.05, 'changes': 12.55}]
# asd.reverse()
# print(asd)
#
# print(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))
# from datetime import timezone
# print('{:.4f}'.format(1.0))
# print(datetime.now().astimezone(timezone.utc))
#

import re
from datetime import datetime, date, time
from base.db_interactions.sql_model import PgsqlCRUD


class MassModel(list):
    def delete(self):
        if self != []:
            id_list = [obj_mod.id for obj_mod in self]
            return self[0]._Model__mass_delete(id__in=id_list)
        else:
            return False

    def sorted_by(self, *args, desc=False):
        sort_func = lambda x: [getattr(x, arg) for arg in args]
        return sorted(self, key=sort_func, reverse=desc)



class Model:
    table_name = 'table_name'

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
            'in': ' in ({}) and ',
            'gt': ' > {} and ',
            'gte': ' >= {} and ',
            'lt': ' < {} and ',
            'lte': ' <= {} and ',
            'like': ' like {} and ',
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
                return particles[0], particles[0] + ' = {} and ', particles[1]
        except:
            return field_name, field_name + ' = {} and ', None

    @staticmethod
    def formate_value(field_type, value):
        obj_type = field_type.obj_type
        if obj_type == str:
            return f"'{value}'"
        elif obj_type == int:
            return int(value)
        elif obj_type == float:
            return float(value)
        elif obj_type == datetime:
            first_var = re.findall(r'^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}', str(value))
            second_var = re.findall(r'^[\d]{4}-[\d]{2}-[\d]{2}$', str(value))
            if first_var:
                return f"timestamp'{value}'"
            elif second_var:
                return f"date'{value}'"
            else:
                raise Exception(f"{value} is not correct date(ex. yyyy-mm-dd ) "
                                f"or datetime (ex. yyyy-mm-dd hh:mm:ss)")
        elif obj_type == date:
            if re.findall('^[\d]{4}-[\d]{2}-[\d]{2}$', value):
                return f"date'{value}'"
            else:
                raise Exception(f"{value} is not date (ex. yyyy-mm-dd )")
        elif obj_type == time:
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
                "pgp_sym_encrypt(({})::text, 'HzBvFDHrTAUHjTdSWe8QuTghhByZuiS6', 'cipher-algo=aes256')"
            )
        else:
            return parsed_field

    @staticmethod
    def get_if_foreign_object(field_type, foreign_field, value, in_search=False):

        if in_search:
            gotten_object = field_type.obj_type.filter(**{foreign_field: value})
        else:
            gotten_object = field_type.obj_type.get(**{foreign_field: value})

        if gotten_object and in_search:
            return [part.id for part in gotten_object]
        elif gotten_object:
            return gotten_object.id
        else:
            return 0

    @staticmethod
    def check_creating_list(fields, values):
        given_keys = values.keys()
        for field_name, field_type in fields.items():
            if hasattr(field_type, "auto_fill") and field_type.auto_fill and field_name not in given_keys:
                values[field_name] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elif not field_type.blank and field_name not in str(given_keys):
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
                values_set = list()
                for part in value:
                    if foreign_field:
                        part = cls.get_if_foreign_object(field_type, foreign_field, part)
                    formated_part = cls.formate_value(field_type, part)
                    values_set.append(formated_part)
                else:
                    if not values_set:
                        values_set = ['null']
                search_part += parsed_field.format(', '.join([str(part) for part in values_set]))
            else:
                if foreign_field:
                    value = cls.get_if_foreign_object(field_type, foreign_field, value)
                formated_value = cls.formate_value(field_type, value)
                search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-4]

        return search_part

    def get_search_id_part(self):
        return f' WHERE id = {self.id}'

    def get_set_part(self, fields):
        search_part = 'SET '
        for field_name, field_type in fields.items():
            field_name, parsed_field, _ = self.parse_field(field_name)
            value = getattr(self, field_name)

            parsed_field = self.encrypting_or_not(field_type, parsed_field)
            if value != None:
                formated_value = self.formate_value(field_type, value)
            else:
                formated_value = 'null'

            search_part += parsed_field.format(formated_value)
        else:
            search_part = search_part[:-4]
            search_part = search_part.replace(' and ', ',')

        return search_part

    @classmethod
    def get_values_part(cls, fields, values):
        search_part = '('
        for field_name, field_value in values.items():
            field_name, _, foreign_field = cls.parse_field(field_name)
            field_type = fields[field_name]
            if foreign_field:
                field_value = cls.get_if_foreign_object(field_type, foreign_field, field_value)
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
            select_part += field_name
            select_part = cls.decrypting_or_not(field, field_name, select_part)
            select_part += f' as {field_name}, '
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
        fields_list = [key.split('__')[0] for key in values.keys()]
        fields = ', '.join(fields_list)
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
        # with open('./xxx.txt', 'a') as file:
        #     file.write(str(request) + '\n')
        return cls.parse_sql_response(PgsqlCRUD.pgsql_select(request))

    @classmethod
    def _search_all_request(cls):
        request = \
            cls.get_select_all_part() \
            + cls.get_from_part()

        return cls.parse_sql_response(PgsqlCRUD.pgsql_select(request))

    def _update_request(self, cls):
        fields = cls.get_attrs()
        request = \
            self.get_update_part() \
            + self.get_set_part(fields) \
            + self.get_search_id_part()
        return PgsqlCRUD.pgsql_update(request)

    def _delete_request(self):
        request = \
            'DELETE ' \
            + self.get_from_part() \
            + self.get_search_id_part()
        return PgsqlCRUD.pgsql_delete(request)

    @classmethod
    def _insert_request(cls, given_values):
        fields = cls.get_attrs()
        given_values = cls.check_creating_list(fields, given_values)
        request = \
            cls.get_insert_part(given_values) + \
            'VALUES ' + \
            cls.get_values_part(fields, given_values)

        if PgsqlCRUD.pgsql_insert(request):
            return cls.get(**given_values)
        else:
            return None

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

        if PgsqlCRUD.pgsql_insert(request):
            return MassModel([cls.get(**row) for row in given_rows])
        else:
            None

    @classmethod
    def __mass_delete(cls, **kwargs):
        fields = cls.get_attrs()
        request = \
            'DELETE ' \
            + cls.get_from_part() \
            + cls.get_search_part(fields, kwargs)
        return PgsqlCRUD.pgsql_delete(request)

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
        return self._delete_request()

    @classmethod
    def get(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) > 1:
            raise Exception(f"get more then 1 objects {cls}")
        elif len(objects_list) == 0:
            return None
            # raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list[0]

    @classmethod
    def filter(cls, **kwargs):
        objects_list = cls._search_request(kwargs)

        if len(objects_list) == 0:
            return MassModel()
            # raise Exception(f"there is no object with parameters:{kwargs} {cls}")
        else:
            return objects_list

    @classmethod
    def all(cls):
        objects_list = cls._search_all_request()

        if len(objects_list) == 0:
            raise Exception(f"there is no object {cls}")
        else:
            return objects_list


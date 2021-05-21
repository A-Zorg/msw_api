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

class BoolField(GeneralField):
    def __init__(self, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = bool

class ForeignKeyField(GeneralField):
    def __init__(self, table_cls, is_encoded=False, blank=False):
        super().__init__(is_encoded, blank)
        self.obj_type = table_cls
        self.sql_formate = 'int'

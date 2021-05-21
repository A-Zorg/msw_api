from base.db_interactions.models import Model
from base.db_interactions.fields import (
    TextField,
    IntField,
    FloatField,
    DateField,
    DateTimeField,
    TimeField,
    ForeignKeyField,
    BoolField
)


class User(Model):
    table_name = 'index_customuser'
    id_atr = IntField(blank=True)
    password_atr = TextField()
    last_login_atr = DateTimeField(blank=True)
    is_superuser_atr = BoolField(blank=True)
    username_atr = TextField()
    first_name_atr = TextField(blank=True)
    last_name_atr = TextField(blank=True)
    email_atr = TextField(blank=True)
    is_staff_atr = BoolField(blank=True)
    is_active_atr = BoolField(blank=True)
    date_joined_atr = DateTimeField(blank=True)
    hr_id_atr = IntField(blank=True)
    sb_id_atr = IntField(blank=True)
    telegram_id_atr = IntField(blank=True)
    first_work_day_atr = DateTimeField(blank=True)
    fop_atr = BoolField(blank=True)
    patronymic_atr = TextField(blank=True)
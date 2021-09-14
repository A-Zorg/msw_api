from base.db_interactions.models import Model
from base.db_interactions.fields import (
    TextField,
    IntField,
    FloatField,
    DateField,
    DateTimeField,
    TimeField,
    ForeignKeyField
)
from base.db_interactions.index import User


class TraderProfile(Model):
    table_name = 'trader_traderprofile'
    id_atr = IntField(blank=True)
    layout_atr = TextField()
    risk_note_atr = TextField()
    trading_partners_atr = TextField()
    riskblock2_period_atr = IntField()
    last_modified_atr = DateTimeField(auto_fill=True)
    user_id_atr = ForeignKeyField(User)


class RiskBlockPeriod(Model):
    table_name = 'trader_riskblock2periods'
    id_atr = IntField(blank=True)
    user_id_atr = ForeignKeyField(User)
    riskblock2_period_atr = IntField()
    risk_manager_id_atr = ForeignKeyField(User)
    created_at_atr = DateTimeField(auto_fill=True)
    last_modified_atr = DateTimeField(auto_fill=True)

class Log(Model):
    table_name = 'trader_log'
    id_atr = IntField(blank=True)
    created_date_atr = DateTimeField()
    log_type_atr = IntField()
    reason_atr = IntField()
    duration_atr = IntField()
    c_loss_atr = IntField(blank=True)
    auto_close_atr = IntField(blank=True)
    poss_loss_atr = IntField(blank=True)
    pos_auto_cls_atr = IntField(blank=True)
    pos_inv_atr = IntField(blank=True)
    months_active_atr = IntField()
    big_input_atr = TextField(blank=True)
    small_input_atr = TextField(blank=True)
    created_at_atr = DateTimeField(auto_fill=True)
    last_modified_atr = DateTimeField(auto_fill=True)
    risk_manager_id_atr = ForeignKeyField(User)
    user_id_atr = ForeignKeyField(User)










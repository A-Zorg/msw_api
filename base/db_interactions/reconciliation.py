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
from base.db_interactions.accounting_system import AccountType


class ReconciliationUserPropaccounts(Model):
    table_name = 'reconciliation_reconciliationuserpropaccount'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=True)
    month_adj_net_atr = FloatField(is_encoded=True, blank=True)
    # summary_by_date_atr = TextField(is_encoded=True, blank=True)
    updated_atr = DateTimeField()
    user_id_atr = ForeignKeyField(User)
    account_type_id_atr = ForeignKeyField(AccountType)

class PropreportsaccountId(Model):
    table_name = 'reconciliation_propreportsaccountid'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=True)
    propreports_id_atr = IntField()
    group_id_atr = IntField()

class UserPropaccounts(Model):
    table_name = 'reconciliation_userpropaccount'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=True)
    daily_gross_atr = FloatField(is_encoded=True, blank=True)
    daily_adj_net_atr = FloatField(is_encoded=True, blank=True)
    daily_unreal_atr = FloatField(is_encoded=True, blank=True)
    month_gross_atr = FloatField(is_encoded=True, blank=True)
    month_unreal_atr = FloatField(is_encoded=True, blank=True)
    month_adj_net_atr = FloatField(is_encoded=True, blank=True)
    effective_date_atr = DateTimeField()
    created_atr = DateTimeField(auto_fill=True)
    user_id_atr = ForeignKeyField(User)
    account_type_id_atr = ForeignKeyField(AccountType)

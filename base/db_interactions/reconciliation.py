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
from base.db_interactions.index import User
from base.db_interactions.accounting_system import AccountType


class ReconciliationUserPropaccounts(Model):
    table_name = 'reconciliation_reconciliationuserpropaccount'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=False)
    month_adj_net_atr = FloatField(is_encoded=False, blank=True)
    # summary_by_date_atr = TextField(is_encoded=False, blank=True)
    updated_atr = DateTimeField()
    user_id_atr = ForeignKeyField(User)
    account_type_id_atr = ForeignKeyField(AccountType)

class PropreportsaccountId(Model):
    table_name = 'reconciliation_propreportsaccountid'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=False)
    propreports_id_atr = IntField()
    group_id_atr = IntField()

class UserPropaccounts(Model):
    table_name = 'reconciliation_userpropaccount'
    id_atr = IntField(blank=True)
    account_atr = TextField(is_encoded=False)
    daily_gross_atr = FloatField(is_encoded=False, blank=True)
    daily_adj_net_atr = FloatField(is_encoded=False, blank=True)
    daily_unreal_atr = FloatField(is_encoded=False, blank=True)
    month_gross_atr = FloatField(is_encoded=False, blank=True)
    month_unreal_atr = FloatField(is_encoded=False, blank=True)
    month_adj_net_atr = FloatField(is_encoded=False, blank=True)
    effective_date_atr = DateTimeField()
    created_atr = DateTimeField(auto_fill=True)
    user_id_atr = ForeignKeyField(User)
    account_type_id_atr = ForeignKeyField(AccountType)

class UserData(Model):
    table_name = 'reconciliation_userdata'
    id_atr = IntField(blank=True)
    prev_month_net_atr = FloatField(is_encoded=False, blank=True)
    account_atr = FloatField(is_encoded=False, blank=True)
    zp_cash_atr = FloatField(is_encoded=False, blank=True)
    podushka_atr = FloatField(is_encoded=False, blank=True)
    account_plus_minus_atr = FloatField(is_encoded=False, blank=True)
    cash_atr = FloatField(is_encoded=False, blank=True)
    social_atr = FloatField(is_encoded=False, blank=True)
    date_reports_atr = DateTimeField(blank=True)
    date_services_atr = DateTimeField(blank=True)
    date_income_data_atr = DateTimeField(blank=True)
    date_account_atr = DateTimeField(blank=True)
    date_reconciliation_atr = DateTimeField(blank=True)
    qty_of_reconciliations_atr = IntField()
    user_id_atr = ForeignKeyField(User)
    compensations_total_atr = FloatField(is_encoded=False, blank=True)
    deadline_atr = FloatField(is_encoded=False, blank=True)
    office_fees_atr = FloatField(is_encoded=False, blank=True)
    payout_rate_atr = FloatField(is_encoded=False, blank=True)
    services_total_atr = FloatField(is_encoded=False, blank=True)
    total_net_month_atr = FloatField(is_encoded=False, blank=True)
    entries_created_atr = BoolField()
    total_sterling_atr = FloatField(is_encoded=False, blank=True)
    total_takion_atr = FloatField(is_encoded=False, blank=True)
    custom_payout_rate_atr = FloatField(is_encoded=False, blank=True)
    custom_podushka_atr = BoolField()

class Services(Model):
    table_name = 'reconciliation_service'
    id_atr = IntField(blank=True)
    name_atr = TextField(is_encoded=False)
    service_type_atr = TextField()
    amount_atr = FloatField(is_encoded=False)
    effective_datetime_atr = DateTimeField()
    created_atr = DateTimeField(auto_fill=True)
    user_id_atr = ForeignKeyField(User)































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


class Broker(Model):
    table_name = 'accounting_system_broker'
    id_atr = IntField(blank=True)
    name_atr = TextField()


class Clearing(Model):
    table_name = 'accounting_system_clearing'
    id_atr = IntField(blank=True)
    name_atr = TextField()


class Company(Model):
    table_name = 'accounting_system_company'
    id_atr = IntField(blank=True)
    name_atr = TextField()


class PropreportsSubdomain(Model):
    table_name = 'accounting_system_propreportssubdomain'
    id_atr = IntField(blank=True)
    subdomain_atr = TextField()
    secrets_section_atr = TextField()


class AccountType(Model):
    table_name = 'accounting_system_accounttype'
    id_atr = IntField(blank=True)
    account_regexp_atr = TextField()
    company_id_atr = ForeignKeyField(Company)
    broker_id_atr = ForeignKeyField(Broker)
    clearing_id_atr = ForeignKeyField(Clearing)
    propreports_subdomain_id_atr = ForeignKeyField(PropreportsSubdomain)


class UserBillType(Model):
    table_name = 'accounting_system_userbilltypes'
    id_atr = IntField(blank=True)
    name_atr = TextField()


class UserBill(Model):
    table_name = 'accounting_system_userbill'
    id_atr = IntField(blank=True)
    amount_atr = FloatField(is_encoded=False)
    bill_id_atr = ForeignKeyField(UserBillType)
    user_id_atr = ForeignKeyField(User)


class CompanyBill(Model):
    table_name = 'accounting_system_companybill'
    id_atr = IntField(blank=True)
    name_atr = TextField()
    amount_atr = FloatField(is_encoded=False)


class ASProcess(Model):
    table_name = 'accounting_system_asprocess'
    id_atr = IntField(blank=True)
    name_atr = TextField()
    description_atr = TextField()


class Entry(Model):
    table_name = 'accounting_system_entry'
    id_atr = IntField(blank=True)
    date_to_execute_atr = DateTimeField()
    description_atr = TextField(blank=True)
    status_atr = IntField()
    created_atr = DateTimeField()


class Transaction(Model):
    table_name = 'accounting_system_transaction'
    id_atr = IntField(blank=True)
    side_atr = IntField()
    amount_atr = FloatField(is_encoded=False)
    currency_atr = TextField()
    rate_to_usd_atr = IntField()
    amount_usd_atr = FloatField(is_encoded=False)
    description_atr = TextField(blank=True)
    created_atr = DateTimeField()
    status_atr = IntField()
    company_bill_id_atr = ForeignKeyField(CompanyBill, blank=True)
    entry_id_atr = ForeignKeyField(Entry)
    initiated_process_id_atr = ForeignKeyField(ASProcess, blank=True)
    initiated_user_id_atr = ForeignKeyField(User, blank=True)
    user_bill_id_atr = ForeignKeyField(UserBill, blank=True)
    account_type_id_atr = ForeignKeyField(AccountType, blank=True)
    account_atr = TextField(is_encoded=False, blank=True)


class HistoryUserBill(Model):
    table_name = 'accounting_system_historyuserbill'
    id_atr = IntField(blank=True)
    model_id_atr = ForeignKeyField(UserBill)
    history_date_atr = DateTimeField()
    history_change_reason_atr = TextField(blank=True)
    caused_by_transaction_atr = IntField(blank=True)
    history_type_atr = TextField()
    history_created_atr = DateTimeField()
    amount_atr = FloatField(is_encoded=False)
    bill_id_atr = ForeignKeyField(UserBillType)
    entry_id_atr = ForeignKeyField(Entry, blank=True)
    user_id_atr = ForeignKeyField(User)


class HistoryCompanyBill(Model):
    table_name = 'accounting_system_historycompanybill'
    id_atr = IntField(blank=True)
    model_id_atr = ForeignKeyField(CompanyBill)
    history_date_atr = DateTimeField()
    history_change_reason_atr = TextField(blank=True)
    caused_by_transaction_atr = IntField(blank=True)
    history_type_atr = TextField()
    history_created_atr = DateTimeField()
    amount_atr = FloatField(is_encoded=False)
    name_atr = TextField()
    entry_id_atr = ForeignKeyField(Entry, blank=True)


class UserMainData(Model):
    table_name = 'accounting_system_usermaindata'
    id_atr = IntField(blank=True)
    unreal_month_atr = FloatField(is_encoded=False, blank=True)
    gross_month_atr = FloatField(is_encoded=False, blank=True)
    adj_net_month_atr = FloatField(is_encoded=False, blank=True)
    services_total_atr = IntField(is_encoded=False, blank=True)
    compensations_total_atr = IntField(is_encoded=False, blank=True)
    office_fees_atr = IntField(is_encoded=False, blank=True)
    prev_month_net_atr = IntField(is_encoded=False, blank=True)
    total_net_month_atr = IntField(is_encoded=False, blank=True)
    deadline_atr = IntField(is_encoded=False, blank=True)
    payout_rate_atr = FloatField(is_encoded=False, blank=True)
    change_plus_minus_atr = IntField(is_encoded=False, blank=True)
    zp_cash_atr = IntField(is_encoded=False, blank=True)
    company_cash_atr = IntField(is_encoded=False, blank=True)
    social_atr = IntField(is_encoded=False, blank=True)
    withdrawal_atr = IntField(is_encoded=False, blank=True)
    effective_date_atr = DateTimeField()
    created_atr = DateTimeField(auto_fill=True)
    user_id_atr = ForeignKeyField(User)


class Process(Model):
    table_name = 'accounting_system_asprocess'
    id_atr = IntField(blank=True)
    name_atr = TextField()
    description_atr = TextField()
































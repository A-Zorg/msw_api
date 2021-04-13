import datetime
from accounting_system.models import AccountType, Clearing, Company, \
    Broker, Entry, Transaction, UserBill, CompanyBill


clearing = Clearing.objects.get(name='default')
company = Company.objects.get(name='EQS')
broker = Broker.objects.get(name='Broker 4')
user_bill = UserBill.objects.get(id='92773')
company_bill = CompanyBill.objects.get(id='111')

acc_type = AccountType.objects.get(
    broker=broker,
    company=company,
    clearing=clearing
)

entry = Entry.objects.create(
    date_to_execute=datetime.datetime.now(),
    status=0
)


transaction_in = Transaction.objects.create(
    entry=entry,
    side=0,
    user_bill=user_bill,
    amount=-333.333,
    currency='USD',
    rate_to_usd=1,
    amount_usd=-333.333,
    account='defaultEQSBroker 4',
    account_type=acc_type,
    status=0,
)

transaction_in = Transaction.objects.create(
    entry=entry,
    side=abs(0-1),
    company_bill=company_bill,
    amount=-333.333,
    currency='USD',
    rate_to_usd=1,
    amount_usd=-333.333,
    status=0,
)









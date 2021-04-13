import datetime
from accounting_system.models import AccountType, Clearing, Company, \
    Broker, Entry, Transaction, UserBill, CompanyBill


clearing = Clearing.objects.get(name='{CLEARING}')
company = Company.objects.get(name='{COMPANY}')
broker = Broker.objects.get(name='{BROKER}')
user_bill = UserBill.objects.get(id='{USER_BILL}')
company_bill = CompanyBill.objects.get(id='{CompanyBill}')

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
    side={SIDE},
    user_bill=user_bill,
    amount={VALUE},
    currency='USD',
    rate_to_usd=1,
    amount_usd={VALUE},
    account='{ACCOUNT_NAME}',
    account_type=acc_type,
    status=0,
)

transaction_in = Transaction.objects.create(
    entry=entry,
    side=abs({SIDE}-1),
    company_bill=company_bill,
    amount={VALUE},
    currency='USD',
    rate_to_usd=1,
    amount_usd={VALUE},
    status=0,
)









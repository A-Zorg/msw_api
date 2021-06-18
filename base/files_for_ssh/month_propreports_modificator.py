import logging
import random
from datetime import datetime, timedelta
import pytz
import pandas
from django_otp.plugins.otp_totp.models import TOTPDevice
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service, UserPropAccount
from accounting_system.models import UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryCompanyBill, HistoryUserBill, ASProcess, Entry, Transaction
from decimal import Decimal
logging.basicConfig(
                    filename="dataset_log.log",
                    format='%(asctime)s (%(filename)s:%(lineno)d  %(threadName)s) %(name)s - %(levelname)s: %(message)s'
                   )
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def csv_file_modificator():
    import datetime
    import random
    import pandas

    phrase = "len(adj_net_list)-adj_net_list.count(0)==1"                            #PHRASE
    adj_net_to_be_modified = eval('["non zero->change", "zero->create"]')        #MODIFICATOR_TYPES
    if "without mod" in phrase:
        return True

    main_list = pandas.read_excel('/home/alex_zatushevkiy/msw_api/month_propreports_template.xlsx')                               #PATH
    columns = list(main_list.columns)
    user_propreports_in_dict = dict()
    for column in columns[1:]:
        user_propreports_in_dict[column] = list(main_list[column])

    for key, adj_net_list in user_propreports_in_dict.items():
        if eval(phrase) and type(key) == datetime.datetime:
            for adj_net_index in range(len(adj_net_list)):
                if 'zero->create' in adj_net_to_be_modified and adj_net_list[adj_net_index]==0:
                    adj_net_to_be_modified.remove('zero->create')
                    adj_net_list[adj_net_index] = random.randint(-100, 100)/4
                    print(adj_net_list)
                    continue
                elif 'non zero->delete' in adj_net_to_be_modified and adj_net_list[adj_net_index]!=0:
                    adj_net_to_be_modified.remove('non zero->delete')
                    adj_net_list[adj_net_index] = 0
                    continue
                elif 'non zero->change' in adj_net_to_be_modified and adj_net_list[adj_net_index]!=0:
                    adj_net_to_be_modified.remove('non zero->change')
                    adj_net_list[adj_net_index]= random.randint(-100, 100)/4
                    continue
            break


    to_modified_user_propreports = pandas.DataFrame(data=user_propreports_in_dict)
    to_modified_user_propreports.to_excel('/home/alex_zatushevkiy/msw_api/month_propreports.xlsx')                                               #PATH



"""Create user bills types and compamy bills"""
user_bills_type = [
    'Investments',
    'SmartPoints',
    'Withdrawal',
    'Account',
    'Cash hub',
    'Current Net balance'
]
try:
    for b_type in user_bills_type:
        bill_type = UserBillTypes.objects.create(name=b_type)
        bill_type.save()
    logger.info('company bills are created')
except:
    logger.error('types bill were created')
# ---------------------
company_bills_type = [
    'Company ServComp',
    'Company Office Fees',
    'Company Net Income',
    'Company Social Fund',
    'Company Daily Net',
    'Operational'
]
try:
    HistoryCompanyBill.objects.all().delete()
    for c_type in company_bills_type:
        company_bill= CompanyBill.objects.get(name=c_type)
        company_bill.amount = 10000
        company_bill.save()
    logger.info('company bills are created')
except:
    logger.error('company bills were created')

"""modify csv file"""
csv_file_modificator()

"""get data(amount) from accounts for last month"""
result_accounts = pandas.read_excel('/home/alex_zatushevkiy/msw_api/month_propreports.xlsx')                                         # path
columns = list(result_accounts.columns)[1:]
account_month_dict = {}
for _, account in result_accounts.iterrows():
    user = CustomUser.objects.get(hr_id = account[columns[0]])
    if not account_month_dict.get(user):
        account_month_dict[user]={}
    acc_name = account[columns[1]]
    try:
        acc_name=int(acc_name)
    except:
        pass

    acc_type = ReconciliationUserPropAccount.objects.get(account=str(acc_name)).account_type
    if not account_month_dict[user].get(acc_type):
        account_month_dict[user][acc_type]={}

    month_dict = {}
    for column in columns[2:]:
        month_dict[column] = account[column]
    account_month_dict[user][acc_type][account[columns[1]]] = month_dict


"""-------------------------------modify UserPropAccount----------------------------------"""
for column in columns[2:]:
    for _, row in result_accounts.iterrows():
        user = CustomUser.objects.get(hr_id=row['hr_id'])

        acc_name = row['account_id']
        try:
            acc_name = int(acc_name)
        except:
            pass
        acc = str(acc_name)
        acc_day = UserPropAccount.objects.get(
            user = user,
            account = acc,
            effective_date = column.date()
        )
        print(column)
        print(row[column])
        if acc_day.daily_adj_net!=int(row[column]):
            if row[column] == 0:
                acc_day.daily_adj_net = None
            else:
                acc_day.daily_adj_net = row[column]
            acc_day.save()




"""work with bills and histories users"""
HistoryUserBill.objects.filter(user__in = account_month_dict.keys()).delete()

for user in account_month_dict.keys():
    for type in UserBillTypes.objects.all():
        if UserBill.objects.filter(user = user, bill = type):
            bill = UserBill.objects.get(user=user, bill=type)
            bill.amount = 0
            bill.save()
        else:
            bill = UserBill.objects.create(user=user, bill=type, amount = 0)
            bill.save()


"---------------------------correct date-----------------------------------"
tod_ay = datetime.today()
month = (tod_ay-timedelta(tod_ay.day+1)).month
year = (tod_ay - timedelta(tod_ay.day+1)).year
back_date = datetime(year, month, 28, 0, 0, 43, 79043) - timedelta(days=30)

for history_bill in HistoryUserBill.objects.filter(user__in = account_month_dict.keys()):
    history_bill.history_date = back_date
    history_bill.save()

for history_comp_bill in HistoryCompanyBill.objects.all():
    history_comp_bill.history_date = back_date
    history_comp_bill.save()


"""----------------------------------------------------------"""
company_bill = CompanyBill.objects.get(name = 'Company Daily Net')
user_bill_type = UserBillTypes.objects.get(name = 'Current Net balance')
process = ASProcess.objects.get(name = 'Propreports Daily Import')
type = 'changed'


def company(datum, side, company_bill, amount, process, broker=None):
    global Entry, Transaction, CompanyBill, HistoryCompanyBill, Decimal
    entry = Entry.objects.create(date_to_execute=datum, status=1)
    transaction = Transaction.objects.create(
                                                entry = entry,
                                                side = side,
                                                company_bill = company_bill,
                                                amount = amount,
                                                currency = 'USD',
                                                rate_to_usd = 1,
                                                amount_usd = amount,
                                                initiated_process = process,
                                                status = 1,
                                                account_type = broker
    )
    bill = CompanyBill.objects.get(name = 'Company Daily Net')
    if side == 1:
        bill.amount += Decimal(amount)
    elif side == 0:
        bill.amount -= Decimal(amount)
    bill.save()

    history = HistoryCompanyBill.objects.create(
                                        history_date = datum,
                                        history_type = '~',
                                        entry = entry,
                                        name = 'Company Daily Net',
                                        amount = bill.amount,
                                        model_id = bill.id,
                                        caused_by_transaction=transaction.id
    )
    entry.save()
    transaction.save()
    history.save()

    return entry

def user_s(datum, entry, side, user_set, process, user_bill_type ):
    global  Transaction, UserBill, HistoryUserBill, Decimal
    for part in user_set:
        user = part[0]
        broker = part[1]
        account = part[2]
        amount = part[3]
        if amount != 0:
            bill = UserBill.objects.get(user = user, bill = user_bill_type)
            bill.amount = bill.amount + Decimal(amount)
            transaction = Transaction.objects.create(
                                                        entry = entry,
                                                        side = side,
                                                        user_bill = bill,
                                                        amount = amount,
                                                        currency = 'USD',
                                                        rate_to_usd = 1,
                                                        amount_usd = amount,
                                                        initiated_process = process,
                                                        status = 1,
                                                        account = account,
                                                        account_type=broker
            )

            history = HistoryUserBill.objects.create(
                history_date=datum,
                history_type='~',
                user=user,
                bill=user_bill_type,
                entry=entry,
                amount=bill.amount,
                model_id=bill.id,
                caused_by_transaction=transaction.id
            )
            bill.save()
            history.save()
            transaction.save()



for datum in columns[2:]:
    datum = datum
    amount_list = {}
    company_in_dict = {}#was list
    for user in account_month_dict.keys():
        for broker in account_month_dict[user]:
            for account in account_month_dict[user][broker]:
                amount = account_month_dict[user][broker][account][datum]
                #
                # if account is not str:
                #     account = str(int(account))
                if not amount_list.get(broker):#add
                    amount_list[broker] = []#add
                amount_list[broker].append([user, broker, account, amount])

                if not company_in_dict.get(broker):
                    company_in_dict[broker] = [0, 0]
                company_in_dict[broker][0] += amount
                if amount != 0:
                    company_in_dict[broker][1] += 1

    # total = sum([i[3] for i in amount_list])
    # key = any([i[3] != 0 for i in amount_list])
    tz = pytz.timezone('Europe/Kiev')
    utc_time = datetime.utcnow()
    mow_time = pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)
    datum = datum.replace(hour=23, minute=59, second=0) - mow_time.utcoffset()
    """--------------------"""
    for broker in company_in_dict:
        amount_broker = company_in_dict[broker][0]
        if company_in_dict[broker][1] != 0:
            company(datum, 1, company_bill, amount_broker, process, broker)
            entry = company(datum.replace(microsecond=10), 0, company_bill, amount_broker, process, broker)#add
            user_s(datum, entry, 1, amount_list[broker], process, user_bill_type)#add
    """----------------------------"""
    # if key:
    #     entry = company(datum, 0, company_bill, total, process)
    #     user_s(datum, entry, 1, amount_list, process, user_bill_type)

"""------------------------"""
HistoryCompanyBill.objects.filter(history_date__gt=datetime.today().replace(hour=0)).delete()
HistoryUserBill.objects.filter(history_date__gt=datetime.today().replace(hour=0)).delete()

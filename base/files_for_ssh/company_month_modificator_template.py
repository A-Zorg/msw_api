import logging
import random
from datetime import datetime, timedelta
import pandas
from django_otp.plugins.otp_totp.models import TOTPDevice
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service, UserPropAccount
from accounting_system.models import UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryCompanyBill, HistoryUserBill, \
    ASProcess, Entry, Transaction, CompanyPropAccountData
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

    phrase = "{PHRASE}"                            #PHRASE
    adj_net_to_be_modified = eval('{MODIFICATOR_TYPES}')        #MODIFICATOR_TYPES
    if "without mod" in phrase:
        return True

    main_list = pandas.read_excel('{PATH}')                               #PATH
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
    to_modified_user_propreports.to_excel('{PATH2}')                                               #PATH

"""Create user bills types and compamy bills"""
user_bills_type = ['Investments','SmartPoints','Withdrawal',
                   'Account','Cash hub','Current Net balance']
try:
    for b_type in user_bills_type:
        bill_type = UserBillTypes.objects.create(name=b_type)
        bill_type.save()
    logger.info('company bills are created')
except:
    logger.error('types bill were created')
# ---------------------
company_bills_type = ['Company ServComp','Company Office Fees','Company Net Income',
                   'Company Social Fund','Company Daily Net', 'Operational']
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
print(result_accounts)

for _, account in result_accounts.iterrows():
    user = CustomUser.objects.get(hr_id = account[columns[0]])
    if not account_month_dict.get(user):
        account_month_dict[user]={}
    acc_name = account[columns[1]]
    try:
        acc_name=int(acc_name)
    except:
        pass

    # acc_type = ReconciliationUserPropAccount.objects.get(account=str(acc_name)).account_type
    # if not account_month_dict[user].get(acc_type):
    #     account_month_dict[user][acc_type]={}

    # month_dict = {}
    # for column in columns[2:]:
    #     month_dict[column] = account[column]
    # account_month_dict[user][acc_type][account[columns[1]]] = month_dict

sum_for_transactions = {}
for column in columns[2:]:
    sum_for_transactions[column] = sum(result_accounts[column])

"""-------------------------------modify UserPropAccount----------------------------------"""
for column in columns[2:]:
    for _, row in result_accounts.iterrows():
        acc_name = row['account_id']
        try:
            acc_name = int(acc_name)
        except:
            pass
        acc = str(acc_name)
        acc_day = CompanyPropAccountData.objects.get(
            account=acc,
            effective_date=column.date()
        )
        if acc_day.daily_adj_net != int(row[column]):
            if row[column] == 0:
                acc_day.daily_adj_net = None
            else:
                acc_day.daily_adj_net = row[column]
            acc_day.save()

"---------------------------correct date-----------------------------------"
tod_ay = datetime.today()
month = (tod_ay-timedelta(tod_ay.day+1)).month
year = (tod_ay - timedelta(tod_ay.day+1)).year
back_date = datetime(year, month, 28, 0, 0, 43, 79043) - timedelta(30)

for history_comp_bill in HistoryCompanyBill.objects.all():
    history_comp_bill.history_date = back_date
    history_comp_bill.save()

"""----------------------------create entries, transactions, correct bill------------------------------"""
process = ASProcess.objects.get(name='Propreports Daily Import')
for datum, acc_sum in sum_for_transactions.items():
    datum = datum + timedelta(hours=20, minutes=59)
    if acc_sum:
        entry = Entry.objects.create(date_to_execute=datum, status=1)
        company_bill = CompanyBill.objects.get(name='Operational')
        transaction = Transaction.objects.create(
            entry=entry,
            side=1,
            company_bill=company_bill,
            amount=acc_sum,
            currency='USD',
            rate_to_usd=1,
            amount_usd=acc_sum,
            initiated_process=process,
            status=1,
        )

        company_bill.amount += Decimal(acc_sum)

        history = HistoryCompanyBill.objects.create(
            history_date=datum,
            history_type='~',
            entry=entry,
            name='Operational',
            amount=company_bill.amount,
            model_id=company_bill.id,
            caused_by_transaction=transaction.id
        )
        company_bill.save()
        entry.save()
        transaction.save()
        history.save()

"""------------------------"""
HistoryCompanyBill.objects.filter(history_date__gt = datetime.today().replace(hour=0)).delete()


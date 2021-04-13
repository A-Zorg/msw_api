import logging
from datetime import datetime, timedelta
import pandas
from django_otp.plugins.otp_totp.models import TOTPDevice
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service, SmartRiskMyAccount, ServicesAndCompensationUpdate, ImportHRUpdate,PropreportsUpdate
from accounting_system.models import UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryCompanyBill, HistoryUserBill, Transaction, AccountType
from accounting.models import UserAccData
import time

logging.basicConfig(
                    filename="dataset_log.log",
                    format='%(asctime)s (%(filename)s:%(lineno)d  %(threadName)s) %(name)s - %(levelname)s: %(message)s'
                   )
logger=logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('start creation of datasets')

def check_bool(b):
    if type(b) == bool:
        return b
    elif b in ['True', 'true']:
        return True
    elif b in ['False', 'false']:
        return False
    else:
        raise Exception ('Value is not boolean!')

def check_date(d):
    if not d:
        return None
    elif type(d) in [datetime, pandas.Timestamp]:
        return d
    else:
        try:
            # date = datetime.fromisoformat(d)
            return d
        except:
            raise Exception('Incorrect date')

def check_recon_quantity(q):
    if not q:
        return 0
    else:
        return q

def clean_history(set_element):
    for i in range(1,len(set_element)):
        set_element[i].delete()


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
                   'Company Social Fund','Company Daily Net']
try:
    HistoryCompanyBill.objects.all().delete()
    for c_type in company_bills_type:
        company_bill= CompanyBill.objects.get(name=c_type)
        company_bill.amount = 10000
        company_bill.save()
    logger.info('company bills are created')
except:
    logger.error('company bills were created')
"""----------------------------------------------------"""



""" -----------------Creation of users, user bills and user_main table"""
result_users = pandas.read_csv('{PATH}users.csv')
result_users['is_active'] = result_users['is_active'].apply(check_bool)
result_users['is_superuser'] = result_users['is_superuser'].apply(check_bool)
result_users['is_staff']= result_users['is_staff'].apply(check_bool)

for index, user in result_users.iterrows():
    try:
        created_user = CustomUser.objects.create(
                                                    id=user['hr_id'],
                                                    username=user['username'],
                                                    email=user['email'],
                                                    first_name=user['first_name'],
                                                    last_name=user['last_name'],
                                                    is_active=user['is_active'],
                                                    is_superuser=user['is_superuser'],
                                                    is_staff=user['is_staff'],
                                                    hr_id=user['hr_id'],
                                                    sb_id=user['sb_id'],
                                                    telegram_id=user['tg_id'],

                                                )

        created_user.set_password(user['password'])
        result_bills = pandas.read_csv('{PATH}user_bills.csv')
        for index, bill in result_bills.iterrows():
            try:
                if bill['user_hr_id'] == created_user.hr_id:
                    created_user_bill = UserBill.objects.create(
                                     user=created_user,
                                     bill=UserBillTypes.objects.get(name=bill['bill_id']),
                                     amount=bill['amount']

                                                            )
                    created_user_bill.save()
                    logger.info(f'user {created_user.hr_id} - bills are created')
            except:
                logger.error(f'{created_user.hr_id} - bill is not created')


        result_main_users = pandas.read_csv('{PATH}main_users.csv')
        for index, main_user in result_main_users.iterrows():
            try:
                if main_user['user_hr_id'] == created_user.hr_id:
                    created_main_user = UserMainData.objects.create(
                                                                    user=created_user,
                                                                    adj_net_month=main_user['adj_net_month'],
                                                                    gross_month=main_user['gross_month'],
                                                                    unreal_month=main_user['unreal_month'],
                                                                    services_total=main_user['services_total'],
                                                                    compensations_total=main_user['compensations_total'],
                                                                    prev_month_net=main_user['prev_month_net'],
                                                                    total_net_month=main_user['total_net_month'],
                                                                    deadline=main_user['deadline'],
                                                                    payout_rate=main_user['payout_rate'],
                                                                    change_plus_minus=main_user['change_plus_minus'],
                                                                    zp_cash=main_user['zp_cash'],
                                                                    company_cash=main_user['company_cash'],
                                                                    social=main_user['social'],
                                                                    withdrawal=main_user['withdrawal'],
                                                                    office_fees=main_user['office_fees'],
                                                                    effective_date=datetime.today()-timedelta(days=62)
                                                        )
                    created_main_user.save()
                    logger.info(f'user {created_user.hr_id} - main_user is created')
            except:
                logger.error(f'{created_user.hr_id} - main_user is not created')

        otp_device = TOTPDevice.objects.create(user = created_user,
                                               name = created_user.username,
                                               confirmed = True
                                               )
        otp_device.save()
        created_user.save()
        logger.info(f'{user} - user is created')
    except:
        logger.error(f'{user} - user is not created')
"""----------------------------------------------------"""

""" -----------------Creation of user accounts and userdata"""
result_accounts = pandas.read_csv('{PATH}accounts.csv')
for index, account in result_accounts.iterrows():
    user = CustomUser.objects.get(hr_id=account['user_hr_id'])
    try:
        summery_by_date = ''
        with open('{PATH}prop.xlsx', 'rb') as file:
            summery_by_date = file.read()

        created_account = ReconciliationUserPropAccount.objects.create(
                                user=user,
                                account=account['account'],
                                account_type=AccountType.objects.get(id=4),
                                month_adj_net=account['month_adj_net'],
                                summary_by_date=summery_by_date,

        )
        created_account.save()
        logger.info(f'{user} - account is created')
    except:
        logger.error(f'{user} - account is not created')
    for bill_type in UserBillTypes.objects.all():
        query_set = HistoryUserBill.objects.filter(user=user, bill=bill_type)
        clean_history(query_set)
result_userdata = pandas.read_csv('{PATH}userdata.csv')
for index, userdata in result_userdata.iterrows():
    try:
        user = CustomUser.objects.get(hr_id=userdata['user_hr_id'])
        created_userdata = UserData.objects.create(
                user=user,
                services_total = userdata['services_total'],
                compensations_total = userdata['compensations_total'],
                office_fees = userdata['office_fees'],
                prev_month_net = userdata['prev_month_net'],
                total_net_month = userdata['total_net_month'],
                podushka = userdata['podushka'],
                zp_cash = userdata['zp_cash'],
                account = userdata['account'],
                account_plus_minus = userdata['account_plus_minus'],
                social = userdata['social'],
                cash = userdata['cash'],
                payout_rate = userdata['payout_rate'],
                deadline = userdata['deadline'],
                date_reports = datetime.today(),
                date_account = datetime.today(),
                date_services = datetime.today(),
                date_income_data = datetime.today(),
                date_reconciliation = datetime.today().replace(microsecond=0),
                qty_of_reconciliations = userdata['qty_of_reconciliations'],

        )
        created_userdata.save()
        logger.info(f'{user} - userdata is created')
    except:
        logger.error(f'{user} - userdata is not created')
"""----------------------------------------------------"""

""" -----------------Clear history---------------------"""
result_accounts = pandas.read_csv('{PATH}accounts.csv')
for index, account in result_accounts.iterrows():
    user = CustomUser.objects.get(hr_id=account['user_hr_id'])
    try:
        for bill_type in UserBillTypes.objects.all():
            query_set = HistoryUserBill.objects.filter(user=user, bill=bill_type)
            clean_history(query_set)
        logger.info(f'history is cleaned')
    except:
        logger.error(f'history is not cleaned')
for bill in company_bills_type:
    query_set = HistoryCompanyBill.objects.filter(name=bill)
    clean_history(query_set)

"--------------------------------------------------------------"
tod_ay = datetime.today()
month = (tod_ay-timedelta(tod_ay.day+1)).month
year = (tod_ay - timedelta(tod_ay.day+1)).year
back_date = datetime(year, month, 28, 0, 0, 43, 79043)

for history_bill in HistoryUserBill.objects.all():
    history_bill.history_date = back_date
    history_bill.save()

for history_comp_bill in HistoryCompanyBill.objects.all():
    history_comp_bill.history_date = back_date
    history_comp_bill.save()
"""------------------------clear tables form prev month-----------------------------"""
from_date = datetime(year, month, 1, 0, 0, 0)
PropreportsUpdate.objects.filter(date_uploaded__gte=from_date).delete()
ServicesAndCompensationUpdate.objects.filter(date_uploaded__gte=from_date).delete()
ImportHRUpdate.objects.filter(date_uploaded__gte=from_date).delete()
SmartRiskMyAccount.objects.filter(date_uploaded__gte=from_date).delete()
"""-------------------------------create servcompfees for user 234275-------------------------------"""
with open('{PATH}manager_id.txt', 'r') as file:
    user_id = int(file.read())
user = CustomUser.objects.get(id=user_id)

UserAccData.objects.filter(user=user).delete()
Service.objects.filter(user=user).delete()

Service.objects.create(user=user,
                       name='SERV',
                       service_type='service',
                       amount=-100,
                       effective_datetime=back_date
                       ).save()
Service.objects.create(user=user,
                       name='COMP',
                       service_type='compensation',
                       amount=200,
                       effective_datetime=back_date
                       ).save()
Service.objects.create(user=user,
                       name='FEE',
                       service_type='fee',
                       amount=-50,
                       effective_datetime=back_date
                       ).save()
ReconciliationUserPropAccount.objects.filter(user=user).delete()
ReconciliationUserPropAccount.objects.create(user=user,
                       account='777',
                       # propreports_subdomain='vector',
                       month_adj_net=0.01,
                       ).save()
userdata_object = UserData.objects.get(user=user)
userdata_object.prev_month_net=1500
userdata_object.podushka=100
userdata_object.account=2000
userdata_object.account_plus_minus=30
userdata_object.cash=1000
userdata_object.social=5
userdata_object.custom_payout_rate=None
userdata_object.date_reconciliation=None
userdata_object.save()
logger.info('finish creation of datasets')

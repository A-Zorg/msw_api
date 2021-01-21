import names
from password_generator import PasswordGenerator
from datetime import datetime
import random
import pandas

email_end = [
    '@gamil.com',
    '@yahoo.com',
    '@hotmail.com',
    '@msn.com'
]




"""--------------------------------------FOR USER CREATION----------------------------------------------------"""
def user_generator(n=10):
    df = {
        'username': [],
        'email': [],
        'password': [],
        'first_name': [],
        'last_name': [],
        'is_active': [],
        'is_superuser': [],
        'is_staff': [],
        'hr_id': [],
        'sb_id': [],
        'tg_id': [],
    }
    for i in range(n):
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        username = first_name+'_'+last_name
        email = username + str(random.randint(10, 99)) + random.choice(email_end)

        pw = PasswordGenerator()
        pw.maxlen = 10
        pw.minlen = 10
        password = pw.generate()

        df['username'].append(username)
        df['email'].append(email)
        df['password'].append(password)
        df['first_name'].append(first_name)
        df['last_name'].append(last_name)
        df['is_active'].append(True)
        df['is_superuser'].append(False)
        df['is_staff'].append(False)
        df['hr_id'].append(90000+i)
        df['sb_id'].append(10000+i)
        df['tg_id'].append(random.randint(10000000, 99999999))
    return df


def bills_generator(user_hr_id_list):
    bill_type_list = ['Investments','SmartPoints','Withdrawal','Account','Cash hub','Current Net balance']
    df = {
        'user_hr_id': [],
        'bill_id': [],
        'amount': [],

    }
    for hr_id in user_hr_id_list:
        for bill_type in bill_type_list:
            df['user_hr_id'].append(hr_id)
            df['bill_id'].append(bill_type)
            if bill_type=='Account':
                df['amount'].append(random.randint(0,1200))
            else:
                df['amount'].append(random.randint(-100, 1200))

    return df

def main_data_generator(user_hr_id_list):
    df = {
            'user_hr_id': [],
            'unreal_daily': [],
            'gross_daily': [],
            'adj_net_daily': [],
            'adj_net_month': [],
            'gross_month': [],
            'unreal_month': [],
            'services_total': [],
            'compensations_total': [],
            'prev_month_net': [],
            'total_net_month': [],
            'deadline': [],
            'payout_rate': [],
            'change_plus_minus': [],
            'zp_cash': [],
            'company_cash': [],
            'social': [],
            'withdrawal': [],
            'office_fees': [],
    }
    for hr_id in user_hr_id_list:
        df['user_hr_id'].append(hr_id)
        df['unreal_daily'].append(random.randint(-100,200))
        df['gross_daily'].append(random.randint(-100,200))
        df['adj_net_daily'].append(random.randint(-100,200))
        df['adj_net_month'].append(random.randint(-1000,2000))
        df['gross_month'].append(random.randint(-100,200))
        df['unreal_month'].append(random.randint(-100,200))
        df['services_total'].append(random.randint(-500,-100))
        df['compensations_total'].append(random.randint(0, 200))
        df['prev_month_net'].append(random.randint(-100, 2000))
        df['total_net_month'].append(random.randint(-500,2000))
        df['deadline'].append(random.randint(1, 2))
        df['payout_rate'].append(0.37)
        df['change_plus_minus'].append(random.randint(-100,200))
        df['zp_cash'].append(random.randint(0,200))
        df['company_cash'].append(random.randint(50,200))
        df['social'].append(random.randint(0,50))
        df['withdrawal'].append(random.randint(0, 200))
        df['office_fees'].append(random.randint(100, 200))
    return df

"""--------------------------------------FOR RECONCILIATION----------------------------------------------------"""

def accounts_generator(user_list, user_main_list):
    brokers = ['vector', 'zim', 'smart','sts' ]
    df = {
        'user_hr_id': [],
        'propreports_subdomain': [],
        'account': [],
        'month_adj_net': [],
        'summary_by_date': [],
    }
    for index, user in user_list.iterrows():
        hr_id = user['hr_id']
        part = 0
        for qty in range(1,3):
            df['user_hr_id'].append(hr_id)
            df['propreports_subdomain'].append(random.choice(brokers))
            df['account'].append('account_'+str(hr_id)+str(qty) )
            for index, user_main in user_main_list.iterrows():
                if user_main['user_hr_id'] == hr_id:
                    adj_net_month = user_main['adj_net_month']
                    if qty == 1:
                        part = random.randint(-500, 2000)
                    else:
                        part = adj_net_month - part
            df['month_adj_net'].append(part)
            df['summary_by_date'].append(datetime.today())
    return df


def userdata_generator(user_list, user_main_list, user_bill, date=datetime.today()):
    df = {
        'user_hr_id': [],
        'services_total': [],
        'compensations_total': [],
        'prev_month_net': [],
        'total_net_month': [],
        'podushka': [],
        'deadline': [],
        'payout_rate': [],
        'zp_cash': [],
        'office_fees': [],
        'account': [],
        'account_plus_minus': [],
        'cash': [],
        'social': [],
        'date_reports': [],
        'date_services': [],
        'date_income_data': [],
        'date_account': [],
        'date_reconciliation': [],
        'qty_of_reconciliations': [],
    }
    for index, user in user_list.iterrows():
        hr_id = user['hr_id']
        services = pandas.read_csv('base/data_set/services.csv')
        for ind, service in services.iterrows():
            if service['UID'] == hr_id:
                services_total = eval(service['SERV and COMP'])[0]

        compensations = pandas.read_csv('base/data_set/services.csv')
        for ind, compensation in compensations.iterrows():
            if compensation['UID'] == hr_id:
                compensations_total = eval(compensation['SERV and COMP'])[1]

        fees = pandas.read_csv('base/data_set/fees.csv')
        for ind, fee in fees.iterrows():
            if fee['hr_id'] == hr_id:
                office_fees = fee['SUM']

        payout_rate = 0.37
        deadline = 1

        for ind, user_main in user_main_list.iterrows():
            if user_main['user_hr_id'] == hr_id:
                prev_month_net = user_main['prev_month_net']
                total_net_month = user_main['adj_net_month']

        for ind, bill in user_bill.iterrows():
            if bill['user_hr_id'] == hr_id and bill['bill_id'] == 'Account':
                account = bill['amount']

        if total_net_month <= 0:
            podushka = total_net_month
            zp_cash = 0
        else:
            podushka = random.randint(0,total_net_month)
            zp_cash = int((total_net_month-podushka) * payout_rate)
        while True:
            if zp_cash == 0  and account<0 :
                account_plus_minus=0
                break
            else:
                account_plus_minus = random.randint(-200,200)
                if account+account_plus_minus>0 and account_plus_minus<=zp_cash:
                    break
        withdrawal = random.randint(0, (zp_cash-account_plus_minus))
        social = zp_cash-account_plus_minus-withdrawal

        df['user_hr_id'].append(hr_id)
        df['services_total'].append(services_total)
        df['compensations_total'].append(compensations_total)
        df['office_fees'].append(office_fees)
        df['prev_month_net'].append(prev_month_net)
        df['total_net_month'].append(total_net_month)
        df['podushka'].append(podushka)
        df['zp_cash'].append(zp_cash)
        df['account'].append(account)
        df['account_plus_minus'].append(account_plus_minus)
        df['social'].append(social)
        df['cash'].append(zp_cash)
        df['payout_rate'].append(payout_rate)
        df['deadline'].append(deadline)
        df['date_reports'].append(date)
        df['date_account'].append(date)
        df['date_services'].append(date)
        df['date_income_data'].append(date)
        df['date_reconciliation'].append(date)
        df['qty_of_reconciliations'].append(1)

    return df
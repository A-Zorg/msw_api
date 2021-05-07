import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil import tz

def data_set_reconciliation():
    user_bills = pd.read_csv('base/data_set/user_bills.csv')
    context_bills={ 90000+i:[] for i in range(len(user_bills.index)//6)}

    utc= timezone.utc
    back_date = datetime(datetime.now().year, datetime.now().month, 1, 20, 59, 59, tzinfo=utc)
    back_date = back_date.astimezone(tz.gettz('Europe/Kiev')).replace(tzinfo=None)
    reconciliation_date = str(back_date - timedelta(1))
    modified_date = reconciliation_date.replace(' ', 'T')

    for _, bill in user_bills.iterrows():
        context_bills[bill['user_hr_id']].insert(0,{bill['bill_id'] : bill['amount']} )
    context_bills['company'] = [
        {'Company ServComp': 10000},
        {'Company Office Fees': 10000},
        {'Company Net Income': 10000},
        {'Company Social Fund': 10000},
        {'Company Daily Net': 10000},
        {'Operational': 10000},
    ]

    context_entries=list()
    userdata = pd.read_csv('base/data_set/userdata.csv')
    for _, data in userdata.iterrows():
        if data['zp_cash'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(data['zp_cash']),
                'Current Net balance',
                'Cash hub',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][0]['Current Net balance']-=data['zp_cash']
            context_bills[user][1]['Cash hub'] += data['zp_cash']

        if data['services_total'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(-data['services_total']),
                'Current Net balance',
                'Company ServComp',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][0]['Current Net balance'] -= -data['services_total']
            context_bills['company'][0]['Company ServComp'] += -data['services_total']
        if data['compensations_total'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(data['compensations_total']),
                'Current Net balance',
                'Company ServComp',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][0]['Current Net balance'] -= -data['compensations_total']
            context_bills['company'][0]['Company ServComp'] += -data['compensations_total']
        if data['total_net_month'] - data['zp_cash'] != 0 and data['total_net_month'] > 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(data['total_net_month'] - data['zp_cash'] - data['podushka']),
                'Current Net balance',
                'Company Net Income',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][0]['Current Net balance'] -= data['total_net_month'] - data['zp_cash'] - data['podushka']
            context_bills['company'][2]['Company Net Income'] += data['total_net_month'] - data['zp_cash'] - data['podushka']

        if data['cash'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                data['cash'],
                'Withdrawal',
                'Cash hub',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][1]['Cash hub'] -= data['cash']
            context_bills[user][3]['Withdrawal'] += data['cash']

        if data['office_fees'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(-data['office_fees']),
                'Company Office Fees',
                'Cash hub',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][1]['Cash hub'] -= -data['office_fees']
            context_bills['company'][1]['Company Office Fees'] += -data['office_fees']

        if data['social'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(data['social']),
                'Company Social Fund',
                'Cash hub',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][1]['Cash hub'] -= data['social']
            context_bills['company'][3]['Company Social Fund'] += data['social']

        if data['account_plus_minus'] != 0:
            user = data['user_hr_id']
            context_entries.append([
                user,
                float(data['account_plus_minus']),
                'Account',
                'Cash hub',
                'Reconciliation',
                'Applied',
                modified_date
            ])
            context_bills[user][1]['Cash hub'] -= data['account_plus_minus']
            context_bills[user][2]['Account'] += data['account_plus_minus']
    return context_bills, context_entries



def add_number_bills(context, bills, entries):
    session = context.fin_user

    url_user = context.custom_config["host"] + 'api/accounting_system/bills/users/'
    url_comp = context.custom_config["host"] + 'api/accounting_system/bills/company/'
    url_report = context.custom_config["host"] + 'api/accounting_system/report_fields/'

    response = session.get(url_user)
    user_bills = eval(response.text)

    response = session.get(url_comp)
    company_bills = eval(response.text)

    response = session.get(url_report)
    userdata_fields = eval(response.text)
    userdata_fields['account_plus_minus'] = userdata_fields['change_plus_minus']
    del userdata_fields['change_plus_minus']
    userdata_fields['cash'] = userdata_fields['withdrawal']
    del userdata_fields['withdrawal']


    for bill in user_bills:
        user_id = int(bill['user'])
        bill_id = int(bill['id'])
        number = int(bill['bill'])-1

        if bills.get(user_id):
            type_bill = list(bills[user_id][number].keys())[0]
            bills[user_id][number]['id'] = bill_id
            for entry in entries:
                if user_id in entry and type_bill in entry:
                    entry.append(bill_id)

    for bill in company_bills:
        company_bill_id = int(bill['id'])
        company_bill_name = bill['name']
        for comp_type_bill in bills['company']:
            if company_bill_name in comp_type_bill:
                comp_type_bill['id'] = company_bill_id
        for entry in entries:
            if company_bill_name in entry:
                entry.append(company_bill_id)

    userdata = pd.read_csv('base/data_set/userdata.csv')
    userdata_dict = dict()

    for _, data in userdata.iterrows():
        copy_userdata_fields = userdata_fields.copy()

        for key in copy_userdata_fields.keys():
            copy_userdata_fields[key] = data.get(key)
        copy_userdata_fields['company_cash'] = data['total_net_month']-data['zp_cash']
        copy_userdata_fields['change_plus_minus'] = copy_userdata_fields['account_plus_minus']
        del copy_userdata_fields['account_plus_minus']
        copy_userdata_fields['withdrawal'] = copy_userdata_fields['cash']
        del copy_userdata_fields['cash']

        userdata_dict[data['user_hr_id']] = copy_userdata_fields
    return bills, entries, userdata_dict


import random
import re
from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import correct_py_file
from behave.api.async_step import async_run_until_complete
import pandas as pd
from datetime import date, datetime, timedelta
from base.sql_functions import pgsql_select, pgsql_update
from base.adminka import finish_reconciliation_process
from base.main_functions import get_token
from base.ssh_interaction import change_db_through_django

def to_float(text):
    return float(text)

def to_list(text):
    return eval(text)

register_type(Number=to_float, List=to_list)

calc_payout_rate = [
    {'from': -10000000, 'to': 0, 'coefficient': 0, 'start': 0},
    {'from': 0, 'to': 20000, 'coefficient': 0.0001, 'start': 37},
    {'from': 20000, 'to':60000, 'coefficient': 0.00015, 'start': 36},
    {'from': 60000, 'to': 100000, 'coefficient': 0.00005, 'start': 42},
    {'from': 100000, 'to': 500000, 'coefficient': 0.000005, 'start': 46.5},
    {'from': 500000, 'to': 1000000, 'coefficient': 0.000002, 'start': 48},
    {'from': 1000000, 'to': 100000000, 'coefficient': 0, 'start': 50}
]


@step("get user and company bill_id")
def step_impl(context):
    for user_id, bills in context.bills.items():
        if user_id == 90000:
            for bill in bills:
                if bill.get('Current Net balance'):
                    context.user_bill_id = str(bill['id'])
        if user_id == 'company':
            for bill in bills:
                if bill.get('Company Daily Net'):
                    context.company_bill_id = str(bill['id'])

@step("create PROPREPORTS entries:-{clearing}-, -{company}-, -{broker}-, -{side}-, -{value}-")
def step_impl(context, clearing, company, broker, side, value):
    old_new_parts={
        '{CLEARING}': clearing,
        '{COMPANY}': company,
        '{BROKER}': broker,
        '{USER_BILL}': context.user_bill_id,
        '{CompanyBill}': context.company_bill_id,
        '{SIDE}': side,
        '{VALUE}': value,
        '{ACCOUNT_NAME}': clearing+company+broker,
    }
    file_name = 'create_propreports_transaction'
    file_dir = './base/files_for_ssh'

    correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("fin_user get {filter} list")
def step_impl(context, filter):
    url = context.custom_config["host"] + f"api/accounting_system/account_type/{filter}/"
    session = context.fin_user
    response = session.get(url)
    context.config.userdata[filter+'_dr'] = response.json()

@step("create url with filters: {company}, {broker}, {clearing}, {side}")
def step_impl(context, **filters):
    for id, bill in context.id_name_bill.items():
        if bill == 'Current Net balance':
            bill_id = id
    url = context.custom_config["host"] + f'api/accounting_system/entries/?user[]=90000&account[]={bill_id}'

    side = filters.pop('side')
    if side != 'all':
        url = url + f'&transaction_side={side}'

    for filter, body in filters.items():
        if body == 'all':
            for part in context.config.userdata[filter + '_dr']:
                url = url + '&acc_' + filter + '[]=' + str(part['id'])
        else:
            for part in context.config.userdata[filter + '_dr']:
                if part['name'] == body:
                    url = url + '&acc_' + filter + '[]=' + str(part['id'])
    context.url = url

@step("by FIN create journal entries report")
def step_impl(context):
    session = context.fin_user
    response = session.get(context.url)
    context.result = response.json()['data']

@step("check actual result of JE report with expected: {result}")
def step_impl(context, result):
    entries_sum = 0
    for entry in context.result:
        amount = entry['transactions'][0]['amount']
        entries_sum += float(amount)
    assert float(result) == entries_sum
@step("get {user_id} user bills: {ub1}, {ub2} and company bill: {cb1}")
def step_impl(context, user_id, ub1, ub2, cb1):
    context.bills_list={}
    for id, bills in context.bills.items():
        if id == int(user_id):
            for bill in bills:
                if bill.get(ub1):
                    context.bills_list['userbill_1'] = [str(bill['id'])]

                elif bill.get(ub2):
                    context.bills_list['userbill_2'] = [str(bill['id'])]
        if id == 'company':
            for bill in bills:
                if bill.get(cb1):
                    context.bills_list['companybill_1'] = [str(bill['id'])]

@step("post request to perform NET buyout: {amount}")
def step_impl(context, amount):
    session = context.super_user
    url = context.custom_config["host"] + 'api/accounting_system/entry/custom/net_buyout/'
    token = get_token(session=session, url=url)

    request_dict = {
        'transaction_out.user_bill': context.bills_list['userbill_2'][0],
        'transaction_out.company_bill': '',
        'transaction_in.user_bill': context.bills_list['userbill_1'][0],
        'transaction_in.company_bill': '',
        'entry.date_to_execute': datetime.now(),
        'entry.description': 'NET buyout',
        'transaction_common.amount_usd': amount,
        'transaction_common.description': 'NET buyout',
        'csrfmiddlewaretoken': token,
    }

    response = session.post(
        url,
        data=request_dict,
        headers={
                "Referer": url,
        }
    )

    context.response_entry = response.json()['entry']

@step("[NET buyout] get bills amount {period} request")
def step_impl(context, period):
    session = context.super_user

    for key, value in context.bills_list.items():
        url = context.custom_config["host"] + f'admin/accounting_system/{key[:-2]}/{value[0]}/change/'
        response = session.get(url)
        text = response.text
        result = re.findall('<input type="number" name="amount" value="([0-9\.-]*)" step=', text)[0]
        value.append(float(result))

@step("check bills after NET buyout: {amount:Number}, {custom_payout:Number}")
def step_impl(context, amount, custom_payout):
    if custom_payout == 0 or amount > 60000:
        for case in calc_payout_rate:
            if case['from'] <= amount < case['to']:
                payout = (case['start'] + case['coefficient']*amount)/100
    else:
        payout = custom_payout

    user_bill_1_before = context.bills_list['userbill_1'][1]
    user_bill_1_after = context.bills_list['userbill_1'][2]
    user_bill_2_before = context.bills_list['userbill_2'][1]
    user_bill_2_after = context.bills_list['userbill_2'][2]
    company_bill_before = context.bills_list['companybill_1'][1]
    company_bill_after= context.bills_list['companybill_1'][2]

    assert round(user_bill_1_before + amount, 4) == user_bill_1_after
    assert round(user_bill_2_before - amount*payout, 4) == user_bill_2_after
    assert round(company_bill_before - amount * (1-payout), 4) == company_bill_after

@step("check transactions after NET buyout")
def step_impl(context):
    request = 'SELECT company_bill_id, user_bill_id FROM public.accounting_system_transaction ' \
              f"WHERE entry_id = '{context.response_entry}'"
    result = pgsql_select(request, **context.custom_config['pg_db'])

    for key, value in context.bills_list.items():
        if value[0] not in str(result):
            assert False
    assert len(result) == 3


@step("[NET buyout] create request boy template")
def step_impl(context):
    context.request_dict = {
        'transaction_out.user_bill': '',
        'transaction_out.company_bill': '',
        'transaction_in.user_bill': '',
        'transaction_in.company_bill': '',
        'entry.date_to_execute': datetime.now(),
        'entry.description': 'NET buyout',
        'transaction_common.amount_usd': 123,
        'transaction_common.description': 'NET buyout',
        'csrfmiddlewaretoken': '',
    }

@step("[NET buyout] change field -{field}- to {value}")
def step_impl(context, field, value):
    if value == "none":
        context.request_dict[field] = ''
    else:
        context.request_dict[field] = value

@step("[NET buyout] field -{field}- == {user_id} {user_bill}")
def step_impl(context, field, user_id, user_bill):
    for id, bills in context.bills.items():
        if id == int(user_id):
            for bill in bills:
                if bill.get(user_bill):
                    context.request_dict[field] = str(bill['id'])

@step("[NET buyout] post request")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + 'api/accounting_system/entry/custom/net_buyout/'
    context.request_dict['csrfmiddlewaretoken'] = get_token(session=session, url=url)

    response = session.post(
        url,
        data=context.request_dict,
        headers={
            "Referer": url,
        }
    )
    context.response_entry = response.text


@step("[AS] download report xlsx")
def step_impl(context):
    session = context.fin_user
    response = session.get(context.url_xlsx)
    assert response.ok

    with open(f'base/data_set/as_report.xlsx', 'wb') as file:
        file.write(response.content)


@step("[AS] compare xlsx with api results")
def step_impl(context):
    xlsx_list = []
    report = pd.read_excel('base/data_set/as_report.xlsx')
    for index, row in report.iterrows():
        for particle in row:
            if particle != '-':
                xlsx_list.append(float(particle))

    api_list = []
    session = context.fin_user
    result = session.get(context.url).json()
    for key, value in result.items():
        api_list.append(float(key))
        for part in value.values():
            for particle in part.values():
                if particle != None:
                    api_list.append(float(particle))

    assert xlsx_list == api_list





















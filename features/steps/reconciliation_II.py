from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
import pandas as pd
from datetime import date, datetime, timedelta
import re
import psycopg2
import mimetypes

"""add mime type to upload .7z"""
mimetypes.add_type('application/x-7z-compressed', '.7z')

"""-------------------------check all_users_data-----------------------------------"""
@step("get all user_data")
def step_impl(context):
    url = context.custom_config["host"] + 'api/reconciliation/all_users_data/'
    response = GetRequest(context.super_user, url)
    context.response_list = response.json_list
    for part in context.response_list:
        del part['date_reconciliation']

@step("get user_data from dataset")
def step_impl(context):
    userdata_set = pd.read_csv('base/data_set/userdata.csv')
    context.data_list=[]
    for _, user_data in userdata_set.iterrows():
        part_dict = {
                    "hr_id": user_data['user_hr_id'],
                    "prev_month_net": f"{int(user_data['prev_month_net'])}.0000",
                    "podushka": f"{int(user_data['podushka'])}.0000",
                    "zp_cash": f"{int(user_data['zp_cash'])}.0000",
                    "total_takion": None,
                    "total_sterling": None,
                    "services_and_compensations_total": float(user_data['services_total']+user_data['compensations_total']),
                    "office_fees": f"{int(user_data['office_fees'])}.0000",
                    "account": f"{int(user_data['account'])}.0000",
                    "account_plus_minus": f"{int(user_data['account_plus_minus'])}.0000",
                    "cash": f"{int(user_data['cash'])}.0000",
                    "social": f"{int(user_data['social'])}.0000",
                    "qty_of_reconciliations": user_data['qty_of_reconciliations']
                   }
        context.data_list.append(part_dict)

@step("compare userdata lists")
def step_impl(context):
    for part in context.data_list:
        if part not in context.response_list:
            assert False
    assert True

"""-------------------------check setting of reconciliation date -----------------------------------"""
@step("pick date of start: {datum}")
def step_impl(context, datum):
    today = date.today()

    if datum == "today":
        request_date = today
    elif datum == "yesterday":
        request_date = today - timedelta(hours=25)
    elif datum == "tomorrow":
        request_date = today + timedelta(hours=25)
    elif datum == "next_month":
        request_date = today + timedelta(weeks=5)
    elif datum == "aftertomorrow":
        request_date = today + timedelta(hours=48)
        if today.month != request_date.month:
            context.scenario.skip(f'too late for selecting reconciliation date({today})')
    context.request_form = {
        'csrfmiddlewaretoken' : '',
        'date_to_start' : str(request_date)
    }

@step("make post request /reconciliation/date_of_reconciliation/")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + 'api/reconciliation/date_of_reconciliation/'

    token = get_token(session, url)
    context.request_form['csrfmiddlewaretoken'] = token

    context.response = session.post(url, data=context.request_form, headers={"Referer": url})

@step("check data of response: {data}")
def step_impl(context, data):
    assert data in context.response.text


"""-------------------------check reports, serv&comp, risk update -----------------------------------"""

@step('check status of "{key}": {answer}')
def step_impl(context, key, answer):
    if key == 'reports update':
        url = context.custom_config["host"] + 'api/reconciliation/reports_update/'
    elif key == 'services and compensations update':
        url = context.custom_config["host"] + 'api/reconciliation/services_compensations/'
    elif key == 'risk update':
        url = context.custom_config["host"] + 'api/reconciliation/status_accounts/'
    response = GetRequest(context.super_user, url)
    assert answer in response.text

@step("activate upload from {key}")
def step_impl(context, key):
    if key == 'propreports':
        url = context.custom_config["host"] + 'api/reconciliation/reports_update/'
    elif key == 'services and compensations googlesheet':
        url = context.custom_config["host"] + 'api/reconciliation/services_compensations/'

    session = context.super_user

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = session.get(url, headers=headers)
    token = re.findall('csrfToken: "([a-zA-Z0-9]*)"', html.text)[0]

    request_head = {'Referer': url,
                    'X-CSRFTOKEN': token,
                    'X-Requested-With': 'XMLHttpRequest',
                    }
    response = session.post(url, headers=request_head)

@step('activate upload through riskbot')
@async_run_until_complete
async def send_fees_to_riskbot(context):
    async with context.tele_user.conversation('sd_test8_bot') as conv:
        await conv.send_message('/start')
        message = await conv.get_response()
        button = find_button([message], 'Загрузить данные по account')
        await button.click()
        await conv.get_response()
        await conv.send_file('base/data_set/fees.7z')
        answer = await conv.get_response()

        assert answer.text == 'Файл успешно загружен, данные для сверки отправлены'

"""_______________________________________check hr import_________________________________________________"""

@step("activate hr_import")
def step_impl(context):
    context.ex_time = datetime.today()

    url = context.custom_config["host"] + "api/reconciliation/import_hr/"
    session = context.super_user
    response = session.get(url)
    assert response.text

@step("clear reconciliationuserpropaccount table")
def step_impl(context):
    with psycopg2.connect(**context.custom_config['pg_db']) as con:
        cur = con.cursor()

        cur.execute("DELETE FROM reconciliation_reconciliationuserpropaccount WHERE id >0")
        con.commit()

        cur.execute("SELECT * FROM reconciliation_reconciliationuserpropaccount")
        rows = cur.fetchall()

        assert len(rows) == 0

@step("check reconciliationuserpropaccount table after hr import")
def step_impl(context):
    with psycopg2.connect(**context.custom_config['pg_db']) as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM reconciliation_reconciliationuserpropaccount")
        rows = cur.fetchall()

        assert len(rows) > 0

"""--------------------------------------check all_users_data/xlsx------------------------------------------------"""

@step("download all_users_data.xlsx")
def step_impl(context):
    url = context.custom_config["host"] + "api/reconciliation/all_users_data/xlsx"
    session = context.super_user
    response = session.get(url)
    assert response.ok

    with open('base/data_set/all_users_data.xlsx', 'wb') as file:
        file.write(response.content)

@step("parse downloaded all_users_data.xlsx to compare with data from /reconciliation/all_users_data/")
def step_impl(context):
    user_bill = pd.read_excel('base/data_set/all_users_data.xlsx')

    def filter(value):
        if value == '-':
            return None
        elif type(value) == datetime:
            return str(value).replace(' ', 'T')
        else:
            return int(value)

    result = []
    for index, part in user_bill.iterrows():
        if index > 195:
            result.append(
                {
                    "hr_id": filter(part['ID']),
                    "podushka": filter(part['Podushka']),
                    "zp_cash": filter(part['ZP cash']),
                    "prev_month_net": filter(part['Prev Month Balance']),
                    "total_takion": filter(part['Takion Total']),
                    "total_sterling": filter(part['Sterling Total']),
                    "services_and_compensations_total": filter(part['Services Total']),
                    "office_fees": filter(part['Office Fees']),
                    "account": filter(part['Account']),
                    "account_plus_minus": filter(part['Change (+/-)']),
                    "cash": filter(part['Take home']),
                    "social": filter(part['Social']),
                    "date_reconciliation": filter(part['Date Reconciliation']),
                }
            )
    context.actual_result = result[:-1]

@step("compare downloaded data with data from /reconciliation/all_users_data/")
def step_impl(context):
    url = context.custom_config["host"] + "api/reconciliation/all_users_data/"
    session = context.super_user
    response = GetRequest(session, url)
    expected_result = response.json_list

    for part in expected_result:
        del part['qty_of_reconciliations']

    for i in context.actual_result:
        if i not in expected_result:
            assert False
    assert True












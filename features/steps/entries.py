from behave import *
from base.main_functions import GetRequest
import random
from datetime import date, datetime, timedelta
import re
import time


@step("pause - {amount} sec(s)")
def step_impl(context, amount):
    time.sleep(int(amount))
@step("get {subject} number bills")
def step_impl(context, subject):
    if subject == 'user':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/user/types/'
        worker = GetRequest(context.fin_user, url)
        subject_dict = worker.json_list
        context.bill_list = [part['name'] for part in subject_dict]
        context.id_name_bill = {part['id']: part['name'] for part in subject_dict}
    elif subject == 'company':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
        worker = GetRequest(context.fin_user, url)
        subject_dict = worker.json_list
        context.company_bill_list = [part['id'] for part in subject_dict]
        context.company_id_name_bill = {part['id']: part['name'] for part in subject_dict}
@step("define request form")
def step_impl(context):
    context.request = {'transaction_out.user_bill': '',
                       'transaction_out.company_bill': '',
                       'transaction_in.user_bill': '',
                       'transaction_in.company_bill': '',
                       'entry.date_to_execute': '',
                       'entry.description': '',
                       'transaction_common.amount_usd': '',
                       'transaction_common.description': '',
                       'csrfmiddlewaretoken': '', }

@step("random amount pick")
def step_impl(context):
    context.request['transaction_common.amount_usd'] = random.randint(1,10000)

@step("random choice TRANSACTION {direction} {from_bill} bill")
def step_impl(context, direction, from_bill):

    if from_bill == 'user':
        name_user_bill = random.choice(context.bill_list)
        user = random.choice(list(context.modified_bills.keys())[:-1])
        user_bill = [bill for bill in context.modified_bills[user] if bill.get(name_user_bill)][0]
        bill_id = user_bill['id']

        """insert number bill to request form and change amount of bill"""
        if direction == 'FROM':
            context.request['transaction_out.user_bill'] = bill_id
            user_bill[name_user_bill]-=context.request['transaction_common.amount_usd']
        elif direction == 'TO':
            context.request['transaction_in.user_bill'] = bill_id
            user_bill[name_user_bill] += context.request['transaction_common.amount_usd']


    elif from_bill == 'company':
        bill_id = random.choice(context.company_bill_list)
        name_company_bill = context.company_id_name_bill[bill_id]
        company_bill = [bill for bill in context.modified_bills['company'] if bill.get(context.company_id_name_bill[bill_id])][0]

        """insert number bill to request form and change amount of bill"""
        if direction == 'FROM':
            context.request['transaction_out.company_bill'] = bill_id
            company_bill[name_company_bill] -= context.request['transaction_common.amount_usd']
        elif direction == 'TO':
            context.request['transaction_in.company_bill'] = bill_id
            company_bill[name_company_bill] += context.request['transaction_common.amount_usd']

@step("get of {time} date")
def step_impl(context, time):
    if time == 'PAST':
        date_pick = datetime.now()-timedelta(minutes=5)
    elif time == 'FUTURE':
        date_pick = datetime.now() + timedelta(seconds=10)
    context.request['entry.date_to_execute'] = str(date_pick)

@step("get csrf token")
def step_impl(context):
    session = context.super_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
    headers = {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              }
    html = session.get(url, headers=headers)
    token = re.findall('name="csrfmiddlewaretoken" value="(.+)">', html.text)[0]
    context.request['csrfmiddlewaretoken'] = token


@step("make post request to create entry")
def step_impl(context):
    session = context.super_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
    request_dict = context.request
    response = session.post(url, data=request_dict, headers={"Referer": url})
    context.response_entry = eval(response.text)['entry']

@step("check status of entry: {status}")
def step_impl(context, status):
    session = context.super_user
    url = f'https://mytest-server.sg.com.ua:9999/admin/accounting_system/entry/{context.response_entry}/change/'
    worker = GetRequest(session, url)
    html_text = worker.text
    if status =='applied':
        assert 'selected>Applied' in html_text
    elif status =='pending':
        assert 'selected>Pending' in html_text

"""-------------------------------------"""
@step("define template request form")
def step_impl(context):
    session = context.fin_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/users/'
    worker = GetRequest(session, url)
    user_bill = worker.json_list[0]['id']
    context.request = {'transaction_out.user_bill': user_bill,
                       'transaction_out.company_bill': '',
                       'transaction_in.user_bill': '',
                       'transaction_in.company_bill': 111,
                       'entry.date_to_execute': datetime.now()-timedelta(minutes=40),
                       'entry.description': '',
                       'transaction_common.amount_usd': '100',
                       'transaction_common.description': '',
                       'csrfmiddlewaretoken': '', }

@step("make post request")
def step_impl(context):
    session = context.super_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
    request_dict = context.request
    response = session.post(url, data=request_dict, headers={"Referer": url})
    context.response_entry = response.text

@step("change request: field - {field}, value - {value}")
def step_impl(context, field, value):
    if value == 'null':
        value=''
    context.request[field] = value

@step("check actual result with expected {result}")
def step_impl(context, result):
    assert result in context.response_entry


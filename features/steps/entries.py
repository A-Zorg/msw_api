import random
from datetime import datetime, timedelta, timezone
from dateutil import tz
import re
import time
from behave import *
from base.main_functions import GetRequest, get_parts_from_number, get_token
from base.sql_functions import pgsql_select


@step("pause - {amount} sec(s)")
def step_impl(context, amount):
    time.sleep(int(amount))

@step("get {subject} number bills")
def step_impl(context, subject):
    if subject == 'user':
        url = context.custom_config["host"] + 'api/accounting_system/bills/user/types/'
        worker = GetRequest(context.fin_user, url)
        subject_dict = worker.json_list
        context.bill_list = [part['name'] for part in subject_dict]
        context.id_name_bill = {part['id']: part['name'] for part in subject_dict}
    elif subject == 'company':
        url = context.custom_config["host"] + 'api/accounting_system/bills/company/'
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
                       'entry.description': 'autotest',
                       'transaction_common.amount_usd': '',
                       'transaction_common.description': 'autotest',
                       'csrfmiddlewaretoken': '', }

@step("random amount pick")
def step_impl(context):
    context.request['transaction_common.amount_usd'] = random.randint(1, 10000)

"""
Example of context.modified_bills
{90000: [{'Current Net balance': 1540.0, 'id': 42976}, ...
'company': [{'Company ServComp': 11727, 'id': 107},...}
"""

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
            user_bill[name_user_bill] -= context.request['transaction_common.amount_usd']
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

@step("get of {time_} date")
def step_impl(context, time_):
    if time_ == 'PAST':
        context.date_pick = datetime.now()-timedelta(minutes=5)
    elif time_ == 'FUTURE':
        context.date_pick = datetime.now() + timedelta(seconds=10)
    context.request['entry.date_to_execute'] = str(context.date_pick)

@step("get csrf token")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + 'api/accounting_system/entry/'
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
    url = context.custom_config["host"] + 'api/accounting_system/entry/'
    request_dict = context.request
    response = session.post(url, data=request_dict, headers={"Referer": url})
    context.response_entry = eval(response.text)['entry']

@step("check status and datetime of entry: {status}")
def step_impl(context, status):
    session = context.super_user
    url = context.custom_config["host"] + f'admin/accounting_system/entry/{context.response_entry}/change/'
    worker = GetRequest(session, url)
    html_text = worker.text

    entry_datetime = context.date_pick.replace(microsecond=0, tzinfo=tz.gettz('Europe/Kiev'))
    entry_datetime = entry_datetime.astimezone(timezone.utc)
    entry_time = str(entry_datetime.time())
    entry_date = str(entry_datetime.date())

    if status == 'applied':
        assert 'selected>Applied' in html_text
    elif status == 'pending':
        assert 'selected>Pending' in html_text
    assert entry_date in html_text
    assert entry_time in html_text

"""-------------------------------------"""
@step("define template request form")
def step_impl(context):
    session = context.fin_user
    url = context.custom_config["host"] + 'api/accounting_system/bills/users/'
    worker = GetRequest(session, url)
    user_bill = worker.json_list[0]['id']

    url = context.custom_config["host"] + 'api/accounting_system/bills/company/'
    worker = GetRequest(session, url)
    company_bills = worker.json_list

    context.request = {'transaction_out.user_bill': user_bill,
                       'transaction_out.company_bill': '',
                       'transaction_in.user_bill': '',
                       'transaction_in.company_bill': company_bills[0]['id'],
                       'entry.date_to_execute': datetime.now()-timedelta(minutes=40),
                       'entry.description': 'autotest',
                       'transaction_common.amount_usd': '100',
                       'transaction_common.description': 'autotest',
                       'csrfmiddlewaretoken': '',
                       }

@step("make post request")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + 'api/accounting_system/entry/'
    request_dict = context.request
    response = session.post(url, data=request_dict, headers={"Referer": url})
    context.response_entry = response.text

@step("change request: field - {field}, value - {value}")
def step_impl(context, field, value):
    if value == 'del':
        del context.request['transaction_in.user_bill']
        del context.request['transaction_in.company_bill']
    elif value == 'null':
        context.request[field] = ''
    else:
        context.request[field] = value

@step("check actual result with expected {result}")
def step_impl(context, result):
    # if result not in context.response_entry:
    #     with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #         file.write(str(context.response_entry) + '\n')
    assert result in context.response_entry

"""--------------------------------------------MASS TRANSACTION----------------------------------------"""
@step("define request form of mass transaction")
def step_impl(context):
    context.request = {
                        "entry": {
                            "date_to_execute": "",
                            "description": "autotest"
                        },
                        "mass_transaction_out": [],
                        "mass_transaction_in": [],
                        "mass_transaction_common": {
                              "description": "autotest"
                        }
}


@step("get random amount of mass transaction")
def step_impl(context):
    context.transaction_amount = random.randint(100, 10000)


"""
    Example of context.modified_bills
    {90000: [{'Current Net balance': 1540.0, 'id': 42976}, ...
    'company': [{'Company ServComp': 11727, 'id': 107},...}
"""
@step("random choice of MASS TRANSACTION {direction} users bills")
def step_impl(context, direction):
    qty_of_user = random.randint(2,6)
    amounts_list = get_parts_from_number(
                        number = context.transaction_amount,
                        qty=qty_of_user
                    )
    bills_list = []

    for i in range(qty_of_user):
        while True:
            name_user_bill = random.choice(context.bill_list)
            user = random.choice(list(context.modified_bills.keys())[:-1])
            user_bill = [bill for bill in context.modified_bills[user] if bill.get(name_user_bill)][0]
            bill_id = user_bill['id']
            if bill_id not in bills_list:
                bills_list.append(bill_id)

                """modified request form and context.modified_bills"""
                if direction == 'FROM':
                    context.request["mass_transaction_out"].append(
                        {
                            "user_bill": bill_id,
                            "amount_usd": amounts_list[i]
                        }
                    )
                    user_bill[name_user_bill] -= amounts_list[i]
                elif direction == 'TO':
                    context.request["mass_transaction_in"].append(
                        {
                            "user_bill": bill_id,
                            "amount_usd": amounts_list[i]
                        }
                    )
                    user_bill[name_user_bill] += amounts_list[i]
                break

@step("random choice of MASS TRANSACTION {direction} company bill")
def step_impl(context, direction):

    bill_id = random.choice(context.company_bill_list)
    name_company_bill = context.company_id_name_bill[bill_id]
    company_bill = [bill for bill in context.modified_bills['company'] if bill.get(context.company_id_name_bill[bill_id])][0]

    """modified request form and context.modified_bills"""
    if direction == 'FROM':
        context.request["mass_transaction_out"].append(
                        {
                            "company_bill": bill_id,
                            "amount_usd": context.transaction_amount
                        }
        )
        company_bill[name_company_bill] -= context.transaction_amount
    elif direction == 'TO':
        context.request["mass_transaction_in"].append(
                        {
                            "company_bill": bill_id,
                            "amount_usd": context.transaction_amount
                        }
        )
        company_bill[name_company_bill] += context.transaction_amount
@step("get of {time_} date of mass transaction")
def step_impl(context, time_):
    if time_ == 'PAST':
        date_pick = datetime.now()-timedelta(minutes=5)
    elif time_ == 'FUTURE':
        date_pick = datetime.now() + timedelta(seconds=10)
    context.request['entry']['date_to_execute'] = str(date_pick)

@step("make post request to create mass transaction")
def step_impl(context):
    session = context.super_user

    url = context.custom_config["host"] + 'api/accounting_system/entry/multiple_transactions/'
    token = get_token(session=session, url=url)
    request_dict = context.request

    response = session.post(
        url,
        json=request_dict,
        headers={
                "Referer": url,
                "X-CSRFTOKEN": token}
    )

    context.response_entry = eval(response.text)['entry']
    assert response.ok

"""-------------------------------------ERROR OF MASS TRANSACTION--------------------------------------------------"""
@step("define template request form of mass transaction")
def step_impl(context):
    session = context.fin_user

    url = context.custom_config["host"] + 'api/accounting_system/bills/users/'
    worker = GetRequest(session, url)
    user_bills = worker.json_list

    url = context.custom_config["host"] + 'api/accounting_system/bills/company/'
    worker = GetRequest(session, url)
    company_bills = worker.json_list

    context.request = {
        "entry": {
            "date_to_execute": str(datetime.now()),
            "description": "autotest"
        },
        "mass_transaction_out": [
            {
                "user_bill": user_bills[0]['id'],
                "amount_usd": 5
            },
            {
                "user_bill": user_bills[1]['id'],
                "amount_usd": 3
            }
        ],
        "mass_transaction_in": [
            {
                "company_bill": company_bills[0]['id'],
                "amount_usd": 5
            },
            {
                "company_bill": company_bills[1]['id'],
                "amount_usd": 8
            }
        ],
        "mass_transaction_common": {
            "description": "autotest"
        }
    }

@step("change request: {command}")
def step_impl(context, command):
    commands_list = eval(command)
    for comm in commands_list:
        if comm[0] == 'del':
            transaction_side = comm[1][0]
            bill = comm[1][1]
            del context.request[transaction_side][bill]
        elif comm[0] == 'change':
            transaction_side = comm[1][0]
            bill = comm[1][1]
            amount = comm[1][2]
            context.request[transaction_side][bill]["amount_usd"] = amount

@step("post request to create mass transaction")
def step_impl(context):
    session = context.super_user

    url = context.custom_config["host"] + 'api/accounting_system/entry/multiple_transactions/'
    token = get_token(session=session, url=url)
    request_dict = context.request

    response = session.post(
        url,
        json=request_dict,
        headers={
                "Referer": url,
                "X-CSRFTOKEN": token}
    )

    context.response_entry = response.text

"""------------------------------------CANCEL ENTRY--------------------------------------------------"""
@step("define template request form and remember user and company bills: {entry_type} entry")
def step_impl(context, entry_type):
    session = context.fin_user

    url = context.custom_config["host"] + 'api/accounting_system/bills/users/'
    worker = GetRequest(session, url)
    context.user_bill = worker.json_list[0]['id']

    url = context.custom_config["host"] + 'api/accounting_system/bills/company/'
    worker = GetRequest(session, url)
    context.company_bills = worker.json_list[0]['id']

    if entry_type == "applied":
        exec_date = datetime.now()-timedelta(minutes=40)
    elif entry_type == "pending":
        exec_date = datetime.now() + timedelta(minutes=40)

    context.request = {'transaction_out.user_bill': context.user_bill,
                       'transaction_out.company_bill': '',
                       'transaction_in.user_bill': '',
                       'transaction_in.company_bill': context.company_bills,
                       'entry.date_to_execute': exec_date,
                       'entry.description': 'autotest',
                       'transaction_common.amount_usd': '100',
                       'transaction_common.description': 'autotest',
                       'csrfmiddlewaretoken': '',
                       }

@step("get user and company bills {period} canceling entry")
def step_impl(context, period):
    session = context.super_user

    user_bill_url = context.custom_config["host"] + f'admin/accounting_system/userbill/{context.user_bill}/change/'
    response = session.get(user_bill_url).text
    user_bill_amount = re.findall('<input type=\"number\" name=\"amount\" value=\"([0-9\.-]*)\" step=', response)[0]

    user_company_url = context.custom_config["host"] + f'admin/accounting_system/companybill/{context.company_bills}/change/'
    response = session.get(user_company_url).text
    company_bill_amount = re.findall('<input type=\"number\" name=\"amount\" value=\"([0-9\.-]*)\" step=', response)[0]

    if period == 'before':
        context.user_bill_before = float(user_bill_amount)
        context.company_bill_before = float(company_bill_amount)
    elif period == 'after':
        context.user_bill_after = float(user_bill_amount)
        context.company_bill_after = float(company_bill_amount)

@step("cancel the created {entry_type} entry")
def step_impl(context, entry_type):
    entry_id = eval(context.response_entry)['entry']
    session = context.super_user
    url = context.custom_config["host"] + f'api/accounting_system/entry/cancel/{entry_id}/'
    response = session.get(url)

    if entry_type == 'applied':
        context.task_id = response.json()['task_id']
    elif entry_type == 'applied':
        assert response.json()['entry_canceled']

    assert response.json()['type'] == f'Cancel {entry_type} entry'

@step("check status of task")
def step_impl(context):
    if hasattr(context, 'task_id'):
        session = context.super_user
        user_bill_url = context.custom_config["host"] + f'api/accounting_system/task/status/{context.task_id}/'
        response = session.get(user_bill_url).json()

        assert response["status"] == "SUCCESS"

@step("check canceling of entry and transactions")
def step_impl(context):
    entry_id = eval(context.response_entry)['entry']
    request = "SELECT e.status, t.status FROM accounting_system_transaction as t " \
              "JOIN accounting_system_entry as e ON t.entry_id=e.id " \
              f"WHERE e.id = {entry_id}"
    response = pgsql_select(request=request, **context.custom_config['pg_db'])

    for part in response:
        assert part[0] == 3
        assert part[1] == 3

@step("check user and company bills after canceling {entry_type} entry")
def step_impl(context, entry_type):
    if entry_type == 'applied':
        result = float(context.request['transaction_common.amount_usd'])
    elif entry_type == 'pending':
        result = 0
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.user_bill_after)+'\n')
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.user_bill_before)+'\n')
    assert context.user_bill_after - context.user_bill_before == result
    assert context.company_bill_before - context.company_bill_after == result











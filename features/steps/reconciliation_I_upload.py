import random
import json
import re
from behave import *
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
from base.db_interactions.reconciliation import Services, ReconciliationUserPropaccounts
from base.db_interactions.index import User

"""-------------------------activate reconciliation-----------------------------------"""
@step("manager check the status of reconciliation: {answer}")
def step_impl(context, answer):
    url = context.custom_config["host"] + 'api/reconciliation/status/'
    response = GetRequest(context.manager_user, url)
    assert answer in response.text

@step("manager try to perform reconciliation: -{answer}-")
def step_impl(context, answer):
    url = context.custom_config["host"] + 'api/reconciliation/'
    token = get_token(context.manager_user, url)
    request_form = {'csrfmiddlewaretoken': token,
                    'zp_cash': '',
                    'podushka': '',
                    'account_plus_minus': '',
                    'cash': '',
                    'social': '',
                    }

    session = context.manager_user
    response = session.post(url, data=request_form, headers={"Referer": url})
    assert answer in response.text

@step("superuser activate reconciliation")
def step_impl(context):
    url = context.custom_config["host"] + 'api/reconciliation/status/'
    session = context.super_user
    token = get_token(session, url)
    request_form = {'csrfmiddlewaretoken': token,
                    'status': 'true',
                    }
    response = session.post(url, data=request_form, headers={"Referer": url})
    assert 'true' in response.text

"""-------------------------perform reconciliation-----------------------------------"""
@step("get userdata row of the MANAGER")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + 'admin/reconciliation/userdata/'
    worker = GetRequest(session, url)
    html = worker.text
    hr_id = context.custom_config['manager_id']['hr_id']
    context.part_url = re.findall(r'<a href="([a-z0-9/]*)">{0}</a>'.format(hr_id), html)[0]

@step("create url of userdata row and get token")
def step_impl(context):
    context.url = context.custom_config["host"][:-1] + context.part_url
    context.token = get_token(context.super_user, context.url)

@step("define request userdata form")
def step_impl(context):
    context.request = {'user': context.custom_config['manager_id']['user_id'],
                       'csrfmiddlewaretoken':context.token,
                       'prev_month_net': '6000',
                       'account': '1000',
                       'qty_of_reconciliations': '0',
                       '_save': 'Save',
                       }

@step("make correction of userdata form {field} {amount}")
def step_impl(context, field, amount):
    if field != 'none':
        context.request[field] = amount

@step("make post request to change userdata table")
def step_impl(context):
    session = context.super_user
    url = context.url
    request_dict = context.request
    response = session.post(url, data=request_dict, headers={"Referer": url})
    assert response.ok

@step("make post request to make reconciliation {podushka} {zp_cash} {account_plus_minus} {cash} {social}")
def step_impl(context, podushka, zp_cash, account_plus_minus, cash, social):
    url = context.custom_config["host"] + 'api/reconciliation/'
    token = get_token(context.manager_user, url)
    request_form = {'csrfmiddlewaretoken': token,
                    'zp_cash': zp_cash,
                    'podushka': podushka,
                    'account_plus_minus': account_plus_minus,
                    'cash': cash,
                    'social': social,
                    }

    session = context.manager_user
    context.response = session.post(url, data=request_form, headers={"Referer": url})
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(response.status_code)+'\n')

@step("compare result response with expected result {er}")
def step_impl(context, er):
    text = context.response.text
    assert er in text

@step("by RISKMAN make post request to make reconciliation {podushka} {zp_cash} {account_plus_minus} {cash} {social}")
def step_impl(context, podushka, zp_cash, account_plus_minus, cash, social):
    url = context.custom_config["host"] + f'api/reconciliation/{context.custom_config["manager_id"]["hr_id"]}/'
    token = get_token(context.super_user, url)
    request_form = {
        'csrfmiddlewaretoken': token,
        'zp_cash': zp_cash,
        'podushka': podushka,
        'account_plus_minus': account_plus_minus,
        'cash': cash,
        'social': social,
    }

    session = context.super_user
    context.response = session.post(url, data=request_form, headers={"Referer": url})

"""----------------------------------check /reconciliation/user_data/----------------------------------------"""

@step("create expected template of user_data")
def step_impl(context):
    hr_id = int(context.custom_config['manager_id']['hr_id'])
    context.exp_template={
                        "user__hr_id": hr_id,
                        "prev_month_net": 1500,
                        "custom_podushka": False,
                        "podushka": 100,
                        "account": 2000,
                        "account_plus_minus": 30,
                        "social": 5,
                        "cash": 1000,
                        "custom_payout_rate": None,
                        'date_reconciliation': None,
                        "takion_accounts": [
                            {
                                "account": "777",
                                "month_adj_net": 0.01,
                                "summary_by_date": None
                            }
                        ],
                        "sterling_accounts": [
                            # {
                            #     "account": "777",
                            #     "month_adj_net": 0.01,
                            #     "summary_by_date": None
                            # }
                        ],
                        "services": [
                            {
                                "name": "SERV",
                                "amount": -100.0
                            }
                        ],
                        "compensations": [
                            {
                                "name": "COMP",
                                "amount": 200.0
                            }
                        ],
                        "fees": [
                            {
                                "name": "FEE",
                                "amount": -50.0
                            }
                        ]
                    }

@step("get actual template of user_data")
def step_impl(context):
    url = context.custom_config["host"] + "api/reconciliation/user_data/"
    session = context.manager_user
    response = session.get(url)
    context.ac_template = response.json()

@step("by RISKMAN get actual template of user_data")
def step_impl(context):
    url = context.custom_config["host"] + f'api/reconciliation/user_data/{context.custom_config["manager_id"]["hr_id"]}/'
    session = context.super_user
    response = session.get(url)
    context.ac_template = response.json()

@step("compare actual and expected templates")
def step_impl(context):
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.ac_template)+'\n')
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.exp_template)+'\n')
    assert context.ac_template == context.exp_template

"""----------------------------------make questions in MSW----------------------------------------"""

@step("create template for {type_q} question")
def step_impl(context, type_q):
    id = type_q
    context.label = id.replace('_undefined','',)
    context.value = random.randint(1,100)
    context.request_form = {
                                "question_data":[
                                    {
                                        "id": id,
                                        "label": context.label,
                                        "value": context.value
                                    }],


                                "csrfmiddlewaretoken": ""
                            }

@step("make post request to make question")
def step_impl(context):
    url = context.custom_config["host"] + 'api/reconciliation/questions/'
    session = context.manager_user
    token = get_token(session, url)
    context.request_form['csrfmiddlewaretoken'] = token

    json_data = json.dumps(context.request_form)
    response = session.post(url, data=json_data, headers={
        "Referer": url,
        "X-CSRFToken": token,
        'Content-Type': 'application/json;charset=UTF-8'
    })
    assert response.ok

@step('check that {form} comes to telegram_bot {bot}')
@async_run_until_complete
async def send_fees_to_riskbot(context,form, bot):
    if form == 'question':
        question = f"{context.label}: {context.value}"
        header = 'Ваш вопрос из MSW: '
    elif form == 'feedback':
        question = context.text_f
        header = 'Ваш фидбек из MSW'

    messages = await context.tele_user.get_messages(bot,limit=3)
    answer = False
    for message in messages:
        if question and header in message.text:
            answer = True
    assert answer

@step('cancel ticket in telegram_bot {bot}')
@async_run_until_complete
async def send_fees_to_riskbot(context, bot):
    texts=['Отменить тикет', 'Да']
    for text in texts:
        messages = await context.tele_user.get_messages(bot, limit=2)
        for message in messages:
            await message.click(text=text)

"""----------------------------------create feedback in MSW----------------------------------------"""

@step("create template for feedback")
def step_impl(context):
    context.text_f = "asdasdasd"
    context.request_form = {
                                "text": context.text_f
                            }

@step("make post request to create feedback")
def step_impl(context):
    url = context.custom_config["host"] + 'api/reconciliation/feedback/'
    session = context.manager_user
    token = get_token(session, url)

    files={
            'file' : ''
          }
    headers = {
        'Accept': 'application/octet-stream,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/png,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "Referer": url,
        'Content-Type': 'multipart/form-data; boundary=--',
        "X-CSRFToken": token,
    }
    response = session.post(url, data=context.request_form, files=files, headers=headers)
    assert response.ok



@step("delete old services and accounts of user")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    context.user = User.get(id=user_id)
    Services.filter(user_id=context.user).delete()
    ReconciliationUserPropaccounts.filter(user_id=context.user).delete()

@step("create random services, accounts, prev_month_net")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    context.user = User.get(id=user_id)
    Services.filter(user_id=context.user).delete()
    ReconciliationUserPropaccounts.filter(user_id=context.user).delete()







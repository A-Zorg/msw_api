import random
import re
from base64 import b64decode
from behave import *
import json
from behave.api.async_step import async_run_until_complete
from base.main_functions import correct_py_file, get_payout_rate, cut_decimal
from behave.api.async_step import async_run_until_complete
import pandas as pd
from datetime import date, datetime, timedelta
from base.db_interactions.trader_profile import TraderProfile, RiskBlockPeriod, Log
from base.db_interactions.index import User
from base.main_functions import get_token


def to_float(text):
    return float(text)


def to_list(text):
    return eval(text)


register_type(Number=to_float, List=to_list)


@step("Delete manager's row from TraderProfile table")
def step_impl(context):
    context.user_id = context.custom_config['manager_id']['user_id']
    profile_layout = TraderProfile.get(user_id=context.user_id)
    if profile_layout:
        profile_layout.delete()


@step("Delete manager's row from RiskBlockPeriod table")
def step_impl(context):
    context.user_id = context.custom_config['manager_id']['user_id']
    admin_username = context.custom_config['super_user']['username']
    admin = User.get(username=admin_username)
    context.admin_id = admin.id
    user_period = RiskBlockPeriod.get(user_id=context.user_id, risk_manager_id=context.admin_id )
    if user_period:
        user_period.delete()


@step("Make PUT request to api/trader/layout/ by manager")
def step_impl(context):
    url = context.custom_config["host"] + f"api/trader/layout/"
    random_list = [True, False]
    session = context.manager_user
    token = get_token(session=session, url=url, key='X-CSRFToken')

    context.body = [
            {'id': 'R3', 'isHidden': random.choice(random_list)},
            {'id': 'R2', 'isHidden': random.choice(random_list)},
            {'id': 'LP', 'isTall': True, 'isHidden': random.choice(random_list)},
            {'id': 'HR', 'isHidden': random.choice(random_list)},
            {'id': 'R1', 'isHidden': random.choice(random_list)},
            {'id': 'PR', 'isHidden': random.choice(random_list)}
        ]
    random.shuffle(context.body)

    session.put(
        url,
        json={
            'layout': context.body
        },
        headers={
            "Referer": 'https://mytest.sg.com.ua/',
            'X-CSRFToken': token,
        }
    )


@step("Make PUT request to api/trader/risk_block2_period/ by {person}")
def step_impl(context, person):
    url = context.custom_config["host"] + f"api/trader/risk_block2_period/{context.user_id}/"
    if person == 'manager':
        session = context.manager_user
    elif person == 'admin':
        session = context.super_user
    else:
        session = None

    token = get_token(session=session, url=url, key='X-CSRFToken')

    context.body = {
            'riskblock2_period': random.randint(0, 1000)
        }

    response = session.put(
        url,
        json=context.body,
        headers={
            "Referer": 'https://mytest.sg.com.ua/',
            'X-CSRFToken': token,
        }
    )


@step("Check created TraderProfile row: {endpoint}")
def step_impl(context, endpoint):
    if endpoint == 'api/trader/risk_block2_period/':
        url = context.custom_config["host"] + endpoint + f'{context.user_id}/'
    elif endpoint == 'api/trader/layout/':
        url = context.custom_config["host"] + endpoint
    else:
        url = None

    session = context.manager_user
    response = session.get(url)

    if response.json() != context.body:
        context.txt_writer(f'CHECK - {endpoint}')
        context.txt_writer(response.json())
        context.txt_writer(context.body)
        assert False

@step("Check created RiskBlockPeriod row")
def step_impl(context):
    url = context.custom_config["host"] + f'api/trader/risk_block2_period/{context.user_id}/'
    session = context.super_user
    response = session.get(url)

    if response.json() != context.body:
        context.txt_writer(f'CHECK - admin api/trader/risk_block2_period')
        context.txt_writer(response.json())
        context.txt_writer(context.body)
        assert False


def create_log(user_id, manager_id, expired):
    month_active = random.randint(1, 6)
    today = datetime.today()
    if today.month - month_active < 1:
        month = 12 + (today.month - month_active)
        year = today.year - 1
    else:
        month = today.month - month_active
        year = today.year

    created_date = today.replace(month=month, year=year) + \
                   timedelta(days=random.choice([1, 10, 30]) * (1 - 2 * expired))
    log_template = {
        'created_date': created_date,
        'log_type': random.randint(0, 2),
        'reason': random.randint(1, 3),
        'duration': 15,
        'c_loss': random.randint(-10, 99),
        'auto_close': random.randint(-10, 99),
        'poss_loss': random.randint(-10, 99),
        'pos_auto_cls': random.randint(-10, 99),
        'pos_inv': random.randint(-10, 99),
        'months_active': month_active,
        'big_input': 'test: some comment',
        'risk_manager_id': manager_id,
        'user_id': user_id,
    }
    Log.create(**log_template)

    return [expired, log_template]


@step("Create user's logs: {type_creation}")
def step_impl(context, type_creation):
    user_id = context.custom_config['manager_id']['user_id']
    admin_username = context.custom_config['super_user']['username']
    admin = User.get(username=admin_username)
    admin_id = admin.id

    Log.filter(user_id=user_id).delete()

    variants_dict = {
        'one expired and one actual': [True, False],
        'two expired': [True, True],
        'two actual': [False, False],
    }
    context.created_logs = []
    for i in variants_dict[type_creation]:
        context.created_logs.append(
            create_log(
                user_id=user_id,
                manager_id=admin_id,
                expired=i
            )
        )


@step("Log-status of user should be {answer}")
def step_impl(context, answer):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/main_info/{user_id}/'

    session = context.super_user
    response = session.get(url).json()

    if answer == 'null':
        assert response['status'] == None
    elif answer == 'not null':
        assert response['status'] != None
    elif answer == 'null or not':
        first_log = context.created_logs[0]
        second_log = context.created_logs[1]
        # context.txt_writer(context.created_logs[0])
        # context.txt_writer(context.created_logs[1])
        if first_log[1]['created_date'] > second_log[1]['created_date']:
            if first_log[0]:
                assert response['status'] == None
            else:
                assert response['status'] != None
        else:
            if second_log[0]:
                assert response['status'] == None
            else:
                assert response['status'] != None


@step("get user's data from DB")
def step_impl(context):
    context.exp_data = {}

    user_id = context.custom_config['manager_id']['user_id']
    user = User.get(id=user_id)
    context.exp_data['first_name'] = user.first_name
    context.exp_data['second_name'] = user.last_name
    context.exp_data['hr_id'] = user.hr_id

    session = context.sb
    url = f'https://hrtest-server.sg.com.ua/api/contact/{user.sb_id}'
    photo_id = session.get(url).json()['photo']['id']
    photo_url = url + f'/photo/{photo_id}/download'
    context.exp_data['photo'] = session.get(photo_url).content

    profile = TraderProfile.get(user_id=user_id)
    profile.risk_note = 'risk_note text'
    profile.save()
    context.exp_data['risk_note'] = profile.risk_note


@step("get user's data through api/trader/main_info/")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/main_info/{user_id}/'
    session = context.super_user

    response = session.get(url).json()
    image = response['photo']
    head, body = image.split(',', 1)
    response['photo'] = b64decode(body)
    del response['status']

    context.act_data = response


@step("Main-info: compare actual and expected data")
def step_impl(context):
    if context.act_data != context.exp_data:
        context.txt_writer("trader/main_info/: data is not matched")
        assert False












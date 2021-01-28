from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button, get_last_email
from behave.api.async_step import async_run_until_complete
import pandas as pd
from datetime import date, datetime, timedelta
import requests
import re
import pyotp
import configparser

config = configparser.ConfigParser()
config.read("cred/config.ini")

"""-----------------------------------perform login-----------------------------------------------"""
@step("logout manager")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/logout/'
    session = context.manager_user
    response = session.get(url)

    assert response.ok
    context.manager_user = requests.Session()
@step("get {part} token for authentication")
def step_impl(context, part):
    url = f'https://mytest-server.sg.com.ua:9999/api/{part}/'
    session = context.manager_user
    response = session.options(url)

    context.token = response.json()['csrfmiddlewaretoken']

    assert response.ok

@step("perform login by manager")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/login/'
    session = context.manager_user

    user_data={
        'username' : config['manager_user']['username'],
        'password': config['manager_user']['password'],
        'csrfmiddlewaretoken': context.token,
    }
    response = session.post(url, data=user_data, headers={"Referer": 'https://mytest.sg.com.ua:9999/login'})

    assert response.ok

@step("perform token auth. by manager")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/2fa/'
    session = context.manager_user
    totp = config['manager_user']['totp']
    totp_code = pyotp.TOTP(totp)
    current_token = totp_code.now()


    user_data={
        'token' : current_token,
        'csrfmiddlewaretoken': context.token,
    }

    headers={
        "Referer": url,
    }
    response = session.post(url, data=user_data, headers=headers)

    assert response.ok

"""----------------------------------change password-----------------------------------"""

@step("alien get login token for authentication")
def step_impl(context):
    url = f'https://mytest-server.sg.com.ua:9999/api/login/'
    context.session = requests.Session()
    response = context.session.options(url)

    context.token = response.json()['csrfmiddlewaretoken']

    assert response.ok

@step("send message to the manager\'s email")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/index/reset_password/case/'
    session = context.session

    datum={
        'email' : config['email']['username'],
        'csrfmiddlewaretoken': context.token,
        'showLogin' : 'false'
    }

    response = session.post(url, data=datum, headers={"Referer": url})

    assert response.ok

@step('get "change password" key in Riskbot')
@async_run_until_complete
async def send_fees_to_riskbot(context):
    messages = await context.tele_user.get_messages('sd_test8_bot', limit = 1)
    message = messages[0]
    context.key = re.findall('ua/reset-password/(.*)\'\)]' , str(message))[0]

    assert 'Привіт! Хтось замовив зміну пароля до твого облікового запису' in message.text \
           and 'Інакше - повідом про цю подію через тікет в Smart.Support.' in message.text

@step('get "change password" key in email')
def step_impl(context):
    email_body = get_last_email(**config['email'])
    context.key = re.findall('ua/reset-password/(.*)', str(email_body))[0]


@step("change username and password to {direction}")
def step_impl(context, direction):
    url = 'https://mytest-server.sg.com.ua:9999/api/index/reset/'+context.key
    session = context.session
    token = get_token(session, url)

    if direction == 'old':
        datum={
            'username' : config['manager_user']['username'],
            'csrfmiddlewaretoken': context.token,
            'password1' : config['manager_user']['password'],
            'password2': config['manager_user']['password']
        }
    elif direction == 'new':
        datum = {
            'username': 'Bob',
            'csrfmiddlewaretoken': context.token,
            'password1': 'zxcqwe123',
            'password2': 'zxcqwe123'
        }

    response = session.post(url, data=datum, headers={"Referer": url})

    assert response.ok















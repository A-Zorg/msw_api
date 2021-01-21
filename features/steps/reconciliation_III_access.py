from behave import *
from base.main_functions import GetRequest, get_token, find_button
import requests

persons={
    'alien' : 'requests.Session()',
    'manager' : 'context.manager_user',
    'risk' : 'context.super_user',
         }


@step("{person} makes {method} request: {part}")
def step_impl(context,person, method, part):
    url = 'https://mytest-server.sg.com.ua:9999/api'+part
    session = eval(persons[person])

    if method == 'get':
        context.response = session.get(url)
    elif  method == 'post':
        context.response = session.post(url)

    if part == '/reconciliation/status/' and method == 'post' and person!='alien':
        token = get_token(session, url)
        data = {
            'csrfmiddlewaretoken':token,
            'status':'false',
        }
        context.response = session.post(url, data=data, headers={"Referer": url})

@step("check response of request: {text} is {boolean}")
def step_impl(context, text, boolean):
    actual_result = text in context.response.text
    assert actual_result == eval(boolean)


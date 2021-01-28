from behave import *
from base.main_functions import GetRequest, get_token, find_button
import requests

persons={
    'alien' : 'requests.Session()',
    'manager' : 'context.manager_user',
    'risk' : 'context.super_user',
    'fin' : 'context.fin_user',
         }

@step("{person} makes request: {part} , result: {code}")
def step_impl(context,person, part, code):
    url = 'https://mytest-server.sg.com.ua:9999/api' + part
    session = eval(persons[person])
    response = session.options(url)

    assert response.status_code == int(code)

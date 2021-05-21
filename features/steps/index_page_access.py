from behave import *
import requests


persons={
    'alien' : 'requests.Session()',
    'manager' : 'context.manager_user',
    'risk' : 'context.super_user',
    'fin' : 'context.fin_user',
         }

@step("{person} makes request: {part} , result: {code}")
def step_impl(context,person, part, code):
    url = context.custom_config["host"] + 'api' + part
    session = eval(persons[person])
    response = session.options(url)

    assert response.status_code == int(code)






from base.db_interactions.accounting_system import Broker
@step("ASDFG")
def step_impl(context):
    a = Broker.create(name='tyo')
    a.name = "fasdfasdf"
    a.save()
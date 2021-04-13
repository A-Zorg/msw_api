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
from base.ssh_interaction import change_db_through_django

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

@step("create url with filters: {company}, {broker}, {clearing}")
def step_impl(context, **filters):
    for id, bill in context.id_name_bill.items():
        if bill == 'Current Net balance':
            bill_id = id
    url = context.custom_config["host"] + f'api/accounting_system/entries/?user[]=90000&account[]={bill_id}'
    for filter, body in filters.items():
        if body == 'all':
            for part in context.config.userdata[filter + '_dr']:
                url = url + '&acc_' + filter + '[]=' +str(part['id'])
        else:
            for part in context.config.userdata[filter + '_dr']:
                if part['name'] == body:
                    url = url + '&acc_' + filter + '[]=' + str(part['id'])
    context.url = url

@step("by FIN create journal entries report")
def step_impl(context):
    session = context.fin_user
    response = session.get(context.url)
    context.result = response.json()

@step("check actual result of JE report with expected: {result}")
def step_impl(context, result):
    entries_sum = 0
    for entry in context.result:
        amount = entry['transactions'][0]['amount']
        entries_sum += float(amount)
    assert float(result) == entries_sum

























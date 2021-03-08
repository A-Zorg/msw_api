from behave import *
from base.main_functions import GetRequest, random_filter_generator, \
    prev_current_date
from datetime import datetime, timedelta

@step("get {subject} bills for reports")
def step_impl(context, subject):
    if subject == 'company':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
    elif subject == 'user':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/user/types/'
    worker = GetRequest(context.fin_user, url)
    subject_dict = worker.json_list

    context.bill_list = [part['id'] for part in subject_dict]
    context.id_name_bill = {part['id']: part['name'] for part in subject_dict}


@step("get report_fields")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/report_fields/'

    worker = GetRequest(context.fin_user, url)
    subject_dict = worker.json_list

    context.report_fields_list = [key for key in subject_dict.keys()]


@step("formation of url for report: {key} with {datum} date")
def step_impl(context, key, datum):
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/report/?'
    date_dict = {
        "year": "",
        "month": "",
        "day": "",
    }

    if datum == 'non actual':
        variable_dates = prev_current_date()
        date_dict["year"] = variable_dates["current_year"]
        date_dict["month"] = variable_dates["current_month"]
        date_dict["day"] = 1
        context.new_bills = context.bills if datetime.today().day != 1 else context.modified_bills
    elif datum == 'actual':
        variable_dates = prev_current_date()
        date_dict["year"] = variable_dates["current_year"]
        date_dict["month"] = variable_dates["current_month"]
        date_dict["day"] = variable_dates["current_day"]
        context.new_bills = context.modified_bills

    user_url_list = [f'user[]={i}&' for i in list(context.userdata.keys())]
    user_url = ''.join(user_url_list)

    account_url_list = [f'account[]={i}&' for i in context.bill_list]
    account_url = ''.join(account_url_list)

    field_url_list = [f'field[]={i}&' for i in context.report_fields_list]
    field_url = ''.join(field_url_list)

    if key == 'user':
        user_url, context.picked_users = random_filter_generator(list(context.userdata.keys()), 'user')
    elif key == 'account':
        account_url, context.picked_accounts = random_filter_generator(context.bill_list, 'account')
    elif key == 'field':
        field_url, context.picked_fields = random_filter_generator(context.report_fields_list, 'field')

    context.url= url + user_url + account_url + field_url +\
          f'date={date_dict["year"]}-{date_dict["month"]}-{date_dict["day"]}'


@step("get expected report data: {key}")
def step_impl(context, key):
    bills = context.new_bills
    users = context.picked_users if key == 'user' else list(context.userdata.keys())
    account_ids = context.picked_accounts if key == 'account' else context.bill_list
    fields = context.picked_fields if key == 'field' else context.report_fields_list

    expected_dict={}
    for user in users:
        acc = {}
        for id in account_ids:
            name = context.id_name_bill[id]
            for part in bills[user]:
                if part.get(name):
                    acc[name] = part[name]
        fil = {}
        for field in fields:
            data = context.userdata[user][field]
            fil[field] = data

        expected_dict[str(user)] = {'accounts' : acc, 'fields' : fil}
    context.expected_report = expected_dict

@step("compare expected report and actual report")
def step_impl(context):
    worker = GetRequest(context.fin_user, context.url)
    actual_report = worker.json_list
    expected_report = context.expected_report
    if actual_report != expected_report:
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str(expected_report)+'\n')
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str(actual_report)+'\n')
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str(context.url)+'\n')
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str("----------------------------------------")+'\n')
    assert actual_report == expected_report
"""-------------------------company------------------------------"""
@step("formation of url for company report with {datum} date")
def step_impl(context, datum):
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/report/?user[]=company&'
    date_dict = {
        "year": "",
        "month": "",
        "day": "",
    }

    if datum == 'non actual':
        variable_dates = prev_current_date()
        date_dict["year"] = variable_dates["current_year"]
        date_dict["month"] = variable_dates["current_month"]
        date_dict["day"] = 1
        context.new_bills = context.bills if datetime.today().day != 1 else context.modified_bills
    elif datum == 'actual':
        variable_dates = prev_current_date()
        date_dict["year"] = variable_dates["current_year"]
        date_dict["month"] = variable_dates["current_month"]
        date_dict["day"] = variable_dates["current_day"]
        context.new_bills = context.modified_bills

    account_url, context.picked_accounts = random_filter_generator(context.bill_list, 'account')

    context.url= url + account_url +\
          f'date={date_dict["year"]}-{date_dict["month"]}-{date_dict["day"]}'

@step("get expected company report data")
def step_impl(context):
    bills = context.new_bills
    account_ids = context.picked_accounts
    expected_dict={}

    acc = {}
    for id in account_ids:
        name = context.id_name_bill[id]
        for part in bills['company']:
             if part.get(name):
                 acc[name] = part[name]

    expected_dict['company'] = {'accounts' : acc, 'fields' : {}}
    context.expected_report = expected_dict

































from behave import *
from base.main_functions import GetRequest, random_filter_generator, \
    prev_current_date, check_comming_entries



@step("get {subject} bills")
def step_impl(context, subject):
    if subject == 'company':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
    elif subject == 'user':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/user/types/'

    worker = GetRequest(context.fin_user, url)
    subject_dict = worker.json_list
    context.bill_list = [part['id'] for part in subject_dict]
    context.id_name_bill = {part['id']: part['name'] for part in subject_dict}

@step("create {key} url for journal entries")
def step_impl(context, key):
    if key == 'users':
        user_list = [i for i in context.bills.keys()][:-1]
        url_users, users = random_filter_generator(user_list, 'user')
        context.users = users
    elif key == 'company':
        url_users = 'user[]=company&'

    url_accounts, accounts = random_filter_generator(context.bill_list, 'account')

    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entries/?'\
          +url_users\
          +url_accounts


    context.accounts = [ context.id_name_bill[i] for i in accounts]
    context.url = url


@step("add date to journal entries url")
def step_impl(context):

    date_dict = prev_current_date()

    url_date = f'date_from={date_dict["prev_year"]}-{date_dict["prev_month"]}-28T00:00:00&' \
               f'date_to={date_dict["current_year"]}-{date_dict["current_month"]}-01T00:00:00'
    context.url+=url_date


@step("{subject} entries which {key} chosen")
def step_impl(context, subject, key):

    if subject == 'users':
        first_clean = [ entry for entry in context.entries if entry[0] in context.users]
    elif subject == 'company':
        first_clean = context.entries
    second_clean = [ entry for entry in first_clean if entry[2] in context.accounts or entry[3] in context.accounts]

    if key == "were":
        context.choosen_entries = second_clean
    elif key == "were not" or "weren't":
        context.not_choosen_entries = [ entry for entry in context.entries if entry not in second_clean]


@step("check {key} entries")
def step_impl(context, key):
    worker = GetRequest(context.fin_user, context.url)
    subject_dict = worker.json_list
    entries = context.choosen_entries if key == 'appropriate' else context.not_choosen_entries
    result = check_comming_entries(entries, subject_dict, key)
    assert result
"""-----------------------------------------------------------------"""
@step("create url with {key} date")
def step_impl(context, key):
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entries/?user[]=all&account[]=all&'

    date_dict = prev_current_date()
    if key == 'appropriate':
        url_date = f'date_from={date_dict["prev_year"]}-{date_dict["prev_month"]}-27T00:00:00&' \
                   f'date_to={date_dict["current_year"]}-{date_dict["current_month"]}-01T00:00:00'
    elif key == 'inappropriate':
        url_date = f'date_from={date_dict["prev_year"]}-{date_dict["prev_month"]}-24T00:00:00&' \
                   f'date_to={date_dict["prev_year"]}-{date_dict["prev_month"]}-26T00:00:00'
    context.url = url+url_date

@step("check reconciliation entries with {key} date")
def step_impl(context, key):
    worker = GetRequest(context.fin_user, context.url)
    subject_dict = worker.json_list
    entries = context.entries
    result = check_comming_entries(entries, subject_dict, key)
    assert result

"""-----------------------------------------------------------------"""
@step("picking different time intervals")
def step_impl(context):
    date_dict = prev_current_date()

    context.date_one = f'date_from={date_dict["prev_year"]}-{date_dict["prev_month"]}-25T00:00:00&' \
                       f'date_to={date_dict["prev_year"]}-{date_dict["prev_month"]}-26T00:00:00'
    context.date_two = f'date_from={date_dict["current_year"]}-{date_dict["current_month"]}-{date_dict["current_day"]}T00:00:00&' \
                       f'date_to={date_dict["current_year"]}-{date_dict["current_month"]}-{date_dict["current_day"]}T23:59:59'

@step("result of {key} interval")
def step_impl(context, key):
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entries/?user[]=all&account[]=all&'

    if key == 'first':
        worker = GetRequest(context.fin_user, url + context.date_one)
        subject_dict = worker.json_list
        context.result_first = set(str(part) for part in subject_dict)
    elif key == 'second':
        worker = GetRequest(context.fin_user, url + context.date_two)
        subject_dict = worker.json_list
        context.result_second = set(str(part) for part in subject_dict)


@step("compare results of different time intervals")
def step_impl(context):
    intersect = context.result_first.intersection(context.result_second)
    assert  not intersect

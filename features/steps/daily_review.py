from datetime import datetime, timedelta, time
import re
import random
import pandas
import requests
from behave import *
from base.main_functions import correct_py_file
from base.sql_functions import pgsql_del, pgsql_select, pgsql_select_as_dict
from base.adminka import task_configuration, run_periodic_task, wait_periodictask_to_be_done
from base.ssh_interaction import change_db_through_django


@step("from propreports get data of selected {account} for {selected_data}")
def step_impl(context, account, selected_data):
    session = requests.Session()
    url = context.custom_config['propreports']['host'] + "login.php"
    req_dict = {
        'user': context.custom_config['propreports']['user'],
        'password': context.custom_config['propreports']['password']
    }

    response = session.post(
        url=url,
        data=req_dict
    )
    assert response.status_code
    xls_url = context.custom_config['propreports']['host'] + 'report.php?' \
              f"startDate={context.custom_config['propreports']['execution_date']}" \
              f"&endDate={context.custom_config['propreports']['execution_date']}" \
               '&groupId=-4&accountId=1025&reportType=detailed&mode=1' \
               '&baseCurrency=USD&export=1'

    get_response = session.get(xls_url)
    context.binary_data_response = get_response.content.replace(b'\xff\xfe', b'\xfe\xff', 1)

@step("parse data from xls file")
def step_impl(context):
    prop_data = pandas.read_excel(context.binary_data_response)
    execution_date = datetime.strptime(prop_data.columns[0], '%M/%d/%Y').date()
    ticker = ''
    propreportsdata_list = []
    for index, row in prop_data.iterrows():
        if '  - ' in str(row[0]):
            end = str(row[0]).index('  - ')
            ticker = row[0][0:end]
        key_access = re.findall(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', str(row[0]))
        if key_access:
            moment_time = time.fromisoformat(row[0])
            review_date = execution_date if moment_time < time(10, 0, 0) else execution_date + timedelta(days=1)
            propreportsdata_list.append((
                review_date,
                execution_date,
                moment_time,
                ticker,
                'SMRT046N',
                row[5],
                row[6],
                row[7],
            ))
    context.propreports_result = propreportsdata_list

@step("clear review_propreportsdata db table for {selected_data}")
def step_impl(context, selected_data):
    request ="DELETE FROM public.review_propreportsdata " \
              f"WHERE execution_date = date '{context.custom_config['propreports']['execution_date']}' "
    assert pgsql_del(request, **context.custom_config['pg_db'])

@step("run {task_name} for {selected_data}")
def step_impl(context, task_name, selected_data):
    execution_date = datetime.fromisoformat(context.custom_config['propreports']['execution_date'])
    date_plus = execution_date + timedelta(days=1)
    datum = [str(date_plus.date())]
    session = context.super_user
    task_configuration(session, context.custom_config, task_name, arg=datum)
    assert run_periodic_task(session, context.custom_config)

@step("from db get data of selected {account} for {selected_data}")
def step_impl(context, account, selected_data):
    request = "SELECT review_date, execution_date, execution_time, ticker, account, side, shares_amount, price  " \
               "FROM public.review_propreportsdata " \
               f"WHERE execution_date = date '{context.custom_config['propreports']['execution_date']}'"
    context.db_result = pgsql_select(request, **context.custom_config['pg_db'])

@step("compare data from propreports and db")
def step_impl(context):
    for part in context.propreports_result:
        if part not in context.db_result:
            with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
                file.write(str(part) + '\n')
            assert False


@step("get random ticker (review_date=={execution_date})")
def step_impl(context, execution_date):
    request = "SELECT DISTINCT(ticker) FROM public.review_propreportsdata " \
              f"WHERE execution_date = date '{execution_date}'"
    raw_result = pgsql_select(request, **context.custom_config['pg_db'])
    all_result = [ticker[0] for ticker in raw_result]

    context.ticker = random.choice(all_result)
    # context.ticker = "NCLH"

@step("get from db {req_number} DR_data_tuple: request_#=={number}, review_date=={execution_date}")
def step_impl(context, req_number, number, execution_date):
    sql_requests = pandas.read_csv('./base/DR_sql_requests.csv')
    request = sql_requests['request'][int(number)-1].format(
        ticker=context.ticker,
        review_date=execution_date
    )
    response = pgsql_select(request, **context.custom_config['pg_db'])

    if req_number == 'first':
        context.first_req = response
    elif req_number == 'second':
        context.second_req = response

@step("get from db {req_number} DR_data_dictionary: request_#=={number}, review_date=={execution_date}")
def step_impl(context, req_number, number, execution_date):
    sql_requests = pandas.read_csv('./base/DR_sql_requests.csv')
    request = sql_requests['request'][int(number)-1].format(
        ticker=context.ticker,
        review_date=execution_date
    )
    response = pgsql_select_as_dict(request, **context.custom_config['pg_db'])

    if req_number == 'first':
        context.first_req = response
    elif req_number == 'second':
        context.second_req = response

@step("[DR] check calculation: avg_price ans real in PropreportsData")
def step_impl(context):
    unreal_dict = {}
    for row in context.first_req:
        unreal_dict[row[3]] = [row[4], row[5]]

    avg_lis = []
    real_list = []
    prev_data = None
    prev_pos = 0
    for data in context.second_req:
        try:
            if prev_data['account'] != data['account']:
                prev_data = None
                prev_pos = 0
        except:
            pass
        try:
            if unreal_dict.get(data['account']) and prev_data == None:
                prev_pos = unreal_dict[data['account']][0]
                avg_lis.append(unreal_dict[data['account']][1])
        except:
            pass
        cur_pos = 0

        if (data['side'] == 'T' or data['side'] == 'S'):
            cur_pos = prev_pos - data['shares_amount']
        elif data['side'] == 'B':
            cur_pos = prev_pos + data['shares_amount']

        if prev_pos == 0:
            avg_lis.append(round(data['price'], 7))
        elif prev_pos < 0:
            if cur_pos < prev_pos:
                avg_lis.append(round((avg_lis[-1] * abs(prev_pos) + data['price'] * data['shares_amount']) / (
                            data['shares_amount'] + abs(prev_pos)), 7))
            elif cur_pos > 0:
                avg_lis.append(round(data['price'], 7))
            elif cur_pos > prev_pos:
                avg_lis.append(round(avg_lis[-1], 7))
        elif prev_pos > 0:
            if cur_pos > prev_pos:
                avg_lis.append(round((avg_lis[-1] * abs(prev_pos) + data['price'] * data['shares_amount']) / (
                            data['shares_amount'] + abs(prev_pos)), 7))
            elif cur_pos < 0:
                avg_lis.append(round(data['price'], 7))
            elif cur_pos < prev_pos:
                avg_lis.append(round(avg_lis[-1], 7))

        if prev_pos == 0:
            real_list.append(0)
        elif prev_pos < 0:
            if cur_pos < prev_pos:
                real_list.append(0)
            elif cur_pos > 0:
                real_list.append(round((avg_lis[-2] - data['price']) * abs(prev_pos), 7))
            elif cur_pos > prev_pos:
                real_list.append(round((avg_lis[-2] - data['price']) * data['shares_amount'], 7))
        elif prev_pos > 0:
            if cur_pos > prev_pos:
                real_list.append(0)
            elif cur_pos < 0:
                real_list.append(round(-(avg_lis[-2] - data['price']) * abs(prev_pos), 7))
            elif cur_pos < prev_pos:
                real_list.append(round(-(avg_lis[-2] - data['price']) * data['shares_amount'], 7))

        prev_pos = cur_pos
        prev_data = data
        # with open('./xxx.txt', 'a') as file:
        #     file.write(str(avg_lis[-1]) + str('     ') + str(round(data['avg_price'], 7)) + '\n')
        assert avg_lis[-1] == round(data['avg_price'], 7)
        assert real_list[-1] == round(data['real'], 7)









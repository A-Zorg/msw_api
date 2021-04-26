from datetime import datetime, timedelta, time
import json
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


@step("get random ticker")
def step_impl(context):
    review_date = context.dr_dates['target_date']
    request = "SELECT DISTINCT(ticker) FROM public.review_propreportsdata " \
              f"WHERE execution_date = date '{review_date}'"
    raw_result = pgsql_select(request, **context.custom_config['pg_db'])
    clear_result = [ticker[0] for ticker in raw_result]

    context.ticker = random.choice(clear_result)

    # context.ticker = "ZTO"

@step("get from db {req_number} DR_data_tuple: request_#=={number}, review_date=={review_date}")
def step_impl(context, req_number, number, review_date):
    sql_requests = pandas.read_csv('./base/DR_sql_requests.csv')
    request = sql_requests['request'][int(number)-1].format(
        ticker=context.ticker,
        review_date=review_date
    )
    response = pgsql_select(request, **context.custom_config['pg_db'])

    if req_number == 'first':
        context.first_req = response
    elif req_number == 'second':
        context.second_req = response
    elif req_number == 'third':
        context.third_req = response

@step("get from db {req_number} DR_data_dictionary: request_#=={number}, review_date=={review_date}")
def step_impl(context, req_number, number, review_date):
    sql_requests = pandas.read_csv('./base/DR_sql_requests.csv')
    request = sql_requests['request'][int(number)-1].format(
        ticker=context.ticker,
        review_date=review_date
    )
    response = pgsql_select_as_dict(request, **context.custom_config['pg_db'])

    if req_number == 'first':
        context.first_req = response
    elif req_number == 'second':
        context.second_req = response
    elif req_number == 'third':
        context.third_req = response

@step("[DR] check calculation: avg_price ans real in PropreportsData")
def step_impl(context):
    unreal_dict = {}
    for row in context.sql_responses['first']:
        unreal_dict[row[3]] = [row[4], row[5]]

    avg_lis = []
    real_list = []
    prev_data = None
    prev_pos = 0
    for data in context.sql_responses['second']:
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

        assert avg_lis[-1] == round(data['avg_price'], 7)
        assert real_list[-1] == round(data['real'], 7)

@step("[DR] check calculation: unrealizedpertickeraccount")
def step_impl(context):
    prop_list = context.sql_responses['first']
    account = None
    account_list = []
    expected_list = []
    while prop_list:
        account = prop_list[-1]['account']
        account_list.append(account)
        if prop_list[-1]['position'] != 0:
            expected_list.append([
                prop_list[-1]['account'],
                prop_list[-1]['position'],
                prop_list[-1]['avg_price'],
                True
            ])
        prop_list = [row for row in prop_list if row['account'] != account]

    prev_unreal = context.sql_responses['third']
    for row in prev_unreal:
        if row['account'] not in account_list:
            expected_list.append([
                row['account'],
                row['unreal_position'],
                row['unreal_avg_price'],
                False
            ])

    cur_unreal = context.sql_responses['second']
    actual_list = []
    for row in cur_unreal:
        actual_list.append([
            row['account'],
            row['unreal_position'],
            row['unreal_avg_price'],
            row['traded']
        ])

    for obj in actual_list:
        if obj not in expected_list:
            assert False
    assert True

@step("[DR] check calculation: unrealizedperticker")
def step_impl(context):
    unrealized_sum_expected = 0
    traded_expected = False
    if context.sql_responses['first']:
        unrealized_sum_expected = sum([row['unreal_position']for row in context.sql_responses['first']])
        traded_expected = any([row['traded']for row in context.sql_responses['first']])

    unrealized_sum_actual = context.sql_responses['second'][0]['unrealized_sum']
    traded_actual = context.sql_responses['second'][0]['traded']

    assert unrealized_sum_expected == unrealized_sum_actual
    assert traded_expected == traded_actual


@step("[DR] check calculation: intervalsperticker({session})")
def step_impl(context, session):
    def create_expected_dict (start_time, intervals):
        expected_dict = {}
        for interval in range(intervals):
            interval_date = start_time + timedelta(minutes=interval*5)
            interval_time = str(interval_date.time())
            expected_dict[interval_time] = {
                "position": 0,
                "B": 0,
                "S": 0,
                "T": 0
            }
        return expected_dict

    if session == 'PRE':
        start_time = datetime.fromisoformat('0001-01-01 04:00:00')
        expected_dict = actual_dict = create_expected_dict(start_time, 72)
    elif session == 'INT':
        start_time = datetime.fromisoformat('0001-01-01 10:00:00')
        expected_dict = actual_dict = create_expected_dict(start_time, 72)
    elif session == 'POS':
        start_time = datetime.fromisoformat('0001-01-01 16:00:00')
        expected_dict = actual_dict = create_expected_dict(start_time, 48)

    try:
        prev_position = context.sql_responses['second'][0]['unrealized_sum']
    except:
        prev_position = 0
    prev_interval_position = 0

    for row in context.sql_responses['first']:
        real_time = row['execution_time']
        coef = real_time.minute // 5
        interval_time = str(real_time.replace(minute=coef*5, second=0))
        expected_dict[interval_time][row['side']] += row["shares_amount"]

    for interval in expected_dict.values():
        if prev_position:
            interval['position'] = prev_position + interval['B'] - interval['S'] - interval['T']
            prev_position = 0
        else:
            interval['position'] = prev_interval_position + interval['B'] - interval['S'] - interval['T']
        prev_interval_position = interval['position']

    for row in context.sql_responses['third']:
        actual_dict[str(row['interval_time'])] = {
            "position": row['position'],
            "B": row['buy'],
            "S": row['sell'],
            "T": row['short']
        }
    # if expected_dict != actual_dict:
    #     with open('./xxx.txt', 'a') as file:
    #         file.write(str(expected_dict) + '\n')
    #
    #     with open('./xxx.txt', 'a') as file:
    #         file.write(str(actual_dict) + '\n')
    assert expected_dict == actual_dict

@step("[DR] check calculation: datepertickeraccount")
def step_impl(context):
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.sql_responses['first']) + '\n')
    assert context.sql_responses['first'] == context.sql_responses['second']

@step("[DR] check calculation: dateperticker(result, shares_traded, result_in_points)")
def step_impl(context):
    if context.sql_responses['first'] == [(None, None, None)]:
        first_req = []
    else:
        result = context.sql_responses['first'][0][0]
        shares_traded = context.sql_responses['first'][0][1]
        result_in_points = context.sql_responses['first'][0][2]
        if (abs(result)>=0.2 and shares_traded>=10000) or (abs(result)>=1 and shares_traded<10000):
            to_be_showed = True
        else:
            to_be_showed = False
        first_req = [(result, shares_traded, result_in_points, to_be_showed)]
    assert first_req == context.sql_responses['second']


@step("from db get {response_number} DR_data_dictionary: request_name=={req_name}, review_date=={review_date}, session=={session}")
def step_impl(context, response_number, req_name, review_date, session):
    with open('./base/dr_sql_requests.json', 'r') as json_file:
        sql_requests = json.load(json_file)
    request = sql_requests[req_name]
    session = session.upper()
    if 'and execution_time' in request or 'WHERE execution_time' in request:
        if session == "PRE":
            session = "< time '10:00:00'"
        elif session == "INT":
            session = "< time '16:00:00' and execution_time >= time '10:00:00'"
        elif session == "POS":
            session = ">= time '16:00:00'"

    request = sql_requests[req_name].format(
        ticker=context.ticker,
        review_date=context.dr_dates[review_date],
        session=session
    )
    response = pgsql_select_as_dict(request, **context.custom_config['pg_db'])


    if hasattr(context, 'sql_responses'):
        context.sql_responses[response_number] = response
    else:
        context.sql_responses = {}
        context.sql_responses[response_number] = response

@step("from db get {response_number} DR_data_tuple: request_name=={req_name}, review_date=={review_date}, session=={session}")
def step_impl(context, response_number, req_name, review_date, session):
    with open('./base/dr_sql_requests.json', 'r') as json_file:
        sql_requests = json.load(json_file)
    request = sql_requests[req_name]
    session = session.upper()
    if 'and execution_time' in request or 'WHERE execution_time' in request:
        if session == "PRE":
            session = "< time '10:00:00'"
        elif session == "INT":
            session = "< time '16:00:00' and execution_time >= time '10:00:00'"
        elif session == "POS":
            session = ">= time '16:00:00'"

    request = sql_requests[req_name].format(
        ticker=context.ticker,
        review_date=context.dr_dates[review_date],
        session=session
    )
    response = pgsql_select(request, **context.custom_config['pg_db'])

    if hasattr(context, 'sql_responses'):
        context.sql_responses[response_number] = response
    else:
        context.sql_responses = {}
        context.sql_responses[response_number] = response


























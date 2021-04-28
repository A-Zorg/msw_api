from datetime import datetime, timedelta, time
import json
import re
import random
import numpy
import pandas
import requests
from behave import *
from base.sql_request import dr
from base.tools.dr_fun import get_time_param, previous_business_day, write_log
from base.sql_functions import pgsql_del, pgsql_select, pgsql_select_as_dict
from base.adminka import task_configuration, run_periodic_task


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
    request = "DELETE FROM public.review_propreportsdata " \
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
        with open('./xxx.txt', 'a') as file:
            file.write(str(avg_lis[-1]) +'     '+ str(round(data['avg_price'], 7))+'\n')
        with open('./xxx.txt', 'a') as file:
            file.write(str(real_list[-1]) +'     '+ str(round(data['real'], 7))+'\n')
        with open('./xxx.txt', 'a') as file:
            file.write(str(data['account']) + '\n')
        with open('./xxx.txt', 'a') as file:
            file.write(str(context.ticker) + '\n')

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
    with open('./xxx.txt', 'a') as file:
        file.write(str(context.ticker) + '\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(traded_expected) + '\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(traded_actual) + '\n')
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

    if context.sql_responses['second']:
        second_req = [context.sql_responses['second'][0][0:4]]
    else:
        second_req = []
    with open('./xxx.txt', 'a') as file:
        file.write(str(first_req) + '\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(second_req) + '\n')
    assert first_req == second_req

@step("[DR] check calculation: dateperticker NON(result, shares_traded, result_in_points)")
def step_impl(context):
    if context.sql_responses['third']:
        nonmark = list(context.sql_responses['third'][0])
        nonmark.insert(2, round(float(nonmark.pop(2)),5))
    else:
        return True
    premark = context.sql_responses['first'][0] if context.sql_responses['first'] \
        else (0, 0, 0, 0, 0)
    postmark = context.sql_responses['second'][0] if context.sql_responses['second'] \
        else (0, 0, 0, 0, 0)
    max_pos_dict = {
        abs(premark[4]): premark[4],
        abs(postmark[4]): postmark[4]
    }
    exp_result = [
        premark[0] + postmark[0],
        premark[1] + postmark[1],
        round((nonmark[0] / nonmark[1])*10000, 5),
        any([premark[3], postmark[3]]),
        max_pos_dict[max(max_pos_dict.keys())],
    ]

    assert nonmark == exp_result


@step("[DR] check calculation: dateperticker(result_in_percents, office_volume)")
def step_impl(context):
    try:
        dataperticker = context.sql_responses['second'][0]
    except:
        return True
    ticker_result = dataperticker['result']
    ticker_result_in_percent = round(dataperticker['result_in_percents'], 8)
    ticker_shares = dataperticker['shares_traded']
    ticker_office_volume = round(dataperticker['office_volume'], 8)

    session_data = context.sql_responses['first'][0]
    all_shares = session_data['shares_traded']
    all_pos_result = session_data['pos_total_result']
    all_neg_result = session_data['neg_total_result']

    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(ticker_office_volume) + '\n')

    if ticker_result > 0:
        assert round((ticker_result/all_pos_result)*1000000, 8) == ticker_result_in_percent
    else:
        assert -round((ticker_result/all_neg_result)*1000000, 8) == ticker_result_in_percent

    assert ticker_office_volume == round((ticker_shares / all_shares) * 100, 8)

@step("[DR] check calculation: datapersession")
def step_impl(context):
    exp_result = {
        'shares_traded': context.sql_responses['first'][0][0],
        'pos_total_result': round(context.sql_responses['second'][0][0]*10000,5),
        'neg_total_result': round(context.sql_responses['third'][0][0]*10000,5),
    }
    exp_result['positive_percent'] = round(exp_result['pos_total_result'] * 100 / \
                                     (exp_result['pos_total_result'] - exp_result['neg_total_result']), 7)
    exp_result['negative_percent'] = round(exp_result['neg_total_result'] * 100 / \
                                     (exp_result['neg_total_result'] - exp_result['pos_total_result']), 7)

    act_result = {
        'shares_traded': context.sql_responses['forth'][0]['shares_traded'],
        'pos_total_result': round(context.sql_responses['forth'][0]['pos_total_result'], 5),
        'neg_total_result': round(context.sql_responses['forth'][0]['neg_total_result'], 5),
        'positive_percent': round(context.sql_responses['forth'][0]['positive_percent'], 7),
        'negative_percent': round(context.sql_responses['forth'][0]['negative_percent'], 7),
    }


    with open('./xxx.txt', 'a') as file:
        file.write(str(exp_result) + '\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(act_result) + '\n')
    assert exp_result == act_result



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



















# --------------------------------------------------------------------------review_datapertickeraccount (all columns)---
@given("get random account (review_date: {review_date}, session: {session})")
def step_impl(context, review_date, session):
    context.review_date = review_date
    context.session = session

    sql_request = dr['review_propreportsdata_random_acc']
    raw_result = pgsql_select(sql_request, **context.custom_config['pg_db'],
                              param=[review_date] + get_time_param(session))

    context.account = raw_result[0][0]
    context.ticker = raw_result[0][1]


@step("get actual data from review_datapertickeraccount")
def step_impl(context):
    sql_request = dr['review_datapertickeraccount']
    raw_result = pgsql_select(sql_request, **context.custom_config['pg_db'],
                              param=[context.account, context.review_date])

    actual = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result if dic[3] == context.session]
    context.actual = sorted(actual, key=lambda x: x[0])


@then("check calculation: total_real, total_shares_traded")
def step_impl(context):
    if context.session == 'PRE': execution_date = context.review_date
    else: execution_date = previous_business_day(context.review_date)

    sql_request = dr['calc_real_and_shares_amount']
    raw_result = pgsql_select(sql_request, **context.custom_config['pg_db'],
                              param=[context.account, execution_date] + get_time_param(context.session))

    fact = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result]
    context.fact = sorted(fact, key=lambda x: x[0])

    result = numpy.array_equal(context.actual, context.fact)
    if result: write_log([context.session, context.account, context.ticker])
    else: write_log([context.session, context.account, context.actual, context.fact])

    assert result


# ----------------------------------------------------review_dataperticker (total_real, total_shares_traded, max_pos)---
@given("save input data (review_date: {review_date}, session: {session})")
def step_impl(context, review_date, session):
    context.review_date = review_date
    context.session = session


@step("get actual data from review_dataperticker")
def step_impl(context):
    sql_request = dr['review_dataperticker']
    raw_result = pgsql_select(sql_request, **context.custom_config['pg_db'],
                              param=[context.review_date])

    actual = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result if dic[7] == context.session]
    context.actual = sorted(actual, key=lambda x: x[0])


@then("check calculation: total_real, total_shares_traded, max_pos")
def step_impl(context):
    if context.session == 'PRE': execution_date = context.review_date
    else: execution_date = previous_business_day(context.review_date)

    sql_request = dr['calc_real_shares_max_pos']
    raw_result = pgsql_select(sql_request, **context.custom_config['pg_db'],
                              param=[execution_date] + get_time_param(context.session))

    fact = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result]
    context.fact = sorted(fact, key=lambda x: x[0])

    result = numpy.array_equal(context.actual, context.fact)
    if result: write_log([context.session])
    else: write_log([context.session, context.actual, context.fact])

    assert result

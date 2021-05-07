from behave import *
import random
from datetime import datetime, timedelta
from behave.api.async_step import async_run_until_complete
from openpyxl import load_workbook
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
from base.sql_functions import (
    pgsql_select,
    decode_request,
    encode_request,
    pgsql_insert,
    pgsql_del
)



@step("create manager_user bills: account and withdrawal")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']

    request_bills = "SELECT id FROM accounting_system_userbilltypes WHERE name in ('Account', 'Withdrawal')"
    bills = pgsql_select(request=request_bills, **context.custom_config['pg_db'])

    request_del_history_bills = f"DELETE FROM accounting_system_historyuserbill " \
                        f"WHERE user_id={user_id} and bill_id in({bills[0][0]}, {bills[1][0]})"
    assert pgsql_del(request_del_history_bills, **context.custom_config['pg_db'])

    request_del_bills = f"DELETE FROM accounting_system_userbill " \
                        f"WHERE user_id={user_id} and bill_id in({bills[0][0]}, {bills[1][0]})"
    assert pgsql_del(request_del_bills, **context.custom_config['pg_db'])

    for bill in bills:
        amount = random.randint(-500, 500)/4
        request_create_bills = "INSERT INTO accounting_system_userbill(user_id, bill_id, amount) " \
                               "VALUES " \
                               f"({user_id}, {bill[0]}, =-{amount}-=)"

        request_create_bill = encode_request(context, request_create_bills)
        assert pgsql_insert(request_create_bill, **context.custom_config['pg_db'])

        request_get_bill = "SELECT id FROM public.accounting_system_userbill " \
                           f"WHERE user_id={user_id} and bill_id={bill[0]}"
        bill_id = pgsql_select(request_get_bill, **context.custom_config['pg_db'])[0][0]

        date_now = datetime.now()
        date_past = (date_now - timedelta(days=90)).date()
        date_now = date_now.date()
        request_create_historybill = f"INSERT INTO accounting_system_historyuserbill" \
                                     f"(model_id,history_date,history_type,history_created," \
                                     f"amount,bill_id,user_id) " \
                                     f"VALUES " \
                                     f"({bill_id}, date'{date_past}', '+', date'{date_now}', " \
                                     f"=-{amount}-=, {bill[0]}, {user_id})"
        request_create_historybill = encode_request(context, request_create_historybill)
        assert pgsql_insert(request_create_historybill, **context.custom_config['pg_db'])

        with open('./xxx.txt', 'a') as file:
            file.write(str(request_create_historybill) + '\n')


















@step('upload manager\'s account data through Riskbot')
@async_run_until_complete
async def send_fees_to_riskbot(context):
    archives_list = [
        'base/data_set/prev_acc_fees.7z',
        'base/data_set/next_acc_fees.7z'
    ]
    for path in archives_list:
        async with context.tele_user.conversation(context.custom_config["risk_bot"]) as conv:
            await conv.send_message('/start')
            message = await conv.get_response()
            button = find_button([message], 'Загрузить данные по account')
            await button.click()
            await conv.get_response()
            await conv.send_file(path)
            answer = await conv.get_response()

            assert answer.text == 'Файл успешно загружен, данные для сверки отправлены'

@step("get data from accounting:{type_}")
def step_impl(context, type_):
    if type_ == "account_data":
        url = context.custom_config["host"] + "api/accounting/account_data/"
    elif type_ == "account_queue":
        url = context.custom_config["host"] + "api/accounting/payment_queue_data/"

    session = context.manager_user
    response = session.get(url)
    context.act_data = response.json()

    assert response.ok


@step("in accounting compare s expected with actual {type_}")
def step_impl(context, type_):

    if type_ == "account_data":
        expected_data = context.account_data
    elif type_ == "account_queue":
        expected_data = context.queque_accounting
    assert context.act_data == expected_data

@step("in accounting compare expected with actual {type_} file")
def step_impl(context, type_):

    wb_act = load_workbook(f'base/data_set/{type_}.xlsx')
    ws_act = wb_act.active
    values_act = list(ws_act.values)

    wb_exp = load_workbook(f'base/data_set/{type_}_template.xlsx')
    ws_exp = wb_exp.active
    values_exp = list(ws_exp.values)

    assert values_act == values_exp

@step("download {file} xlsx")
def step_impl(context, file):

    if file == 'account_data':
        url = context.custom_config["host"] + "api/accounting/data_history/xlsx_account/"
    elif file == "account_queue":
        url = context.custom_config["host"] + "api/accounting/data_history/xlsx_payment_queue/"

    session = context.manager_user
    response = session.get(url)
    assert response.ok

    with open(f'base/data_set/{file}.xlsx', 'wb') as file:
        file.write(response.content)



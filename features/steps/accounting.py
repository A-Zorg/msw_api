from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
from openpyxl import load_workbook



@step('upload manager\'s account data through Riskbot')
@async_run_until_complete
async def send_fees_to_riskbot(context):
    archives_list = [
        'base/data_set/prev_acc_fees.7z',
        'base/data_set/next_acc_fees.7z'
    ]
    for path in archives_list:
        async with context.tele_user.conversation('sd_test8_bot') as conv:
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
        url = "https://mytest-server.sg.com.ua:9999/api/accounting/account_data/"
    elif type_ == "account_queue":
        url = "https://mytest-server.sg.com.ua:9999/api/accounting/payment_queue_data/"

    session = context.manager_user
    response = session.get(url)
    context.act_data = response.json()

    assert response.ok


@step("in accounting compare expgected with actual {type_}")
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
        url = "https://mytest-server.sg.com.ua:9999/api/accounting/data_history/xlsx_account/"
    elif file == "account_queue":
        url = "https://mytest-server.sg.com.ua:9999/api/accounting/data_history/xlsx_payment_queue/"

    session = context.manager_user
    response = session.get(url)
    assert response.ok

    with open(f'base/data_set/{file}.xlsx', 'wb') as file:
        file.write(response.content)










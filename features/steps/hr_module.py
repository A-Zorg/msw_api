import random
import re
from behave import *
import dateutil.relativedelta as relativedate
from behave.api.async_step import async_run_until_complete
from base.main_functions import correct_py_file, prev_current_date
from behave.api.async_step import async_run_until_complete
import pandas as pd
from datetime import date, datetime, timedelta
from base.sql_functions import pgsql_select, pgsql_update, pgsql_del
from base.adminka import finish_reconciliation_process
from base.main_functions import get_token
from base.ssh_interaction import change_db_through_django
from base.db_interactions.accounting_system import HistoryUserBill
from base.db_interactions.reconciliation import ReconciliationUserPropaccounts



@step("clear all data related to user: {user}")
def step_impl(context, user):
    hr_id = context.custom_config['sb_user']['hr_id']
    try:
        user_id = pgsql_select(
            request=f'SELECT * FROM public.index_customuser WHERE hr_id = {hr_id}',
            **context.custom_config['pg_db']
        )[0][0]
    except:
        return True
    del_request = f'DELETE FROM public.reconciliation_userdata WHERE user_id = {user_id};'\
                  f'DELETE FROM public.reconciliation_reconciliationuserpropaccount WHERE user_id = {user_id}; ' \
                  f'DELETE FROM public.reconciliation_userpropaccount WHERE user_id = {user_id};' \
                  f'DELETE FROM public.reconciliation_service WHERE user_id = {user_id};' \
                  f'DELETE FROM public.accounting_system_historyuserbill WHERE user_id = {user_id};' \
                  f'DELETE FROM public.accounting_system_transaction ' \
                  f'WHERE user_bill_id in(SELECT id FROM public.accounting_system_userbill WHERE user_id = {user_id});' \
                  f'DELETE FROM public.accounting_system_userbill WHERE user_id = {user_id};' \
                  f'DELETE FROM public.otp_totp_totpdevice WHERE user_id = {user_id};' \
                  f'DELETE FROM public.index_customuser WHERE id = {user_id};'

    assert pgsql_del(request=del_request, ** context.custom_config['pg_db'])

@step("get data from SM about user: {user}")
def step_impl(context, user):
    sb_id = context.custom_config['sb_user']['sb_id']
    session = context.sb
    url = f'https://hrtest-server.sg.com.ua/api/contact/{sb_id}'
    result = session.get(url).json()

    context.sb_user_data = [
        result['id'],
        result['externalId'],
        result['firstName'],
        result['lastName'],
        result['email'],
        result['telegramChatId'],
        result['firstWorkingDate'],
    ]
    for account in result['accounts']:
        acc_id = account['id']
        url_delete = f'https://hrtest-server.sg.com.ua/api/contact/{sb_id}/accounts/{acc_id}?delete='
        result = session.post(url=url_delete)
        assert result.status_code

@step("get data from DB about user: {user}")
def step_impl(context, user):
    hr_id = context.custom_config['sb_user']['hr_id']
    user = pgsql_select(
        request=f'SELECT * FROM public.index_customuser WHERE hr_id = {hr_id}',
        **context.custom_config['pg_db']
    )
    context.db_user_data = [
        user[0][12],
        user[0][11],
        user[0][5],
        user[0][6],
        user[0][7],
        str(user[0][13]),
        str(user[0][14].strftime('%d.%m.%Y %H:%M:%S')),
    ]

@step("compare data from DB and SB")
def step_impl(context):
    assert context.db_user_data == context.sb_user_data

@step("should be created {qty} different bills of user: {user}")
def step_impl(context, qty, user):
    hr_id = context.custom_config['sb_user']['hr_id']
    user_id = pgsql_select(
        request=f'SELECT * FROM public.index_customuser WHERE hr_id = {hr_id}',
        **context.custom_config['pg_db']
    )[0][0]

    user_data = pgsql_select(
        request=f'SELECT bill_id FROM public.accounting_system_userbill WHERE user_id = {user_id}',
        **context.custom_config['pg_db']
    )
    user_data = {i[0] for i in user_data}

    assert len(user_data) == int(qty)

@step("check bills date of creation (should be first day of the month before last)")
def step_impl(context):
    exp_date = datetime.now().replace(day=1) + relativedate.relativedelta(months=-2)
    hr_id = context.custom_config['sb_user']['hr_id']
    histories = HistoryUserBill.filter(user_id__hr_id=hr_id)

    for history in histories:
        assert history.history_date.date() == exp_date.date()

@step("{action} trading account with name {acc_name} to user: {user}")
def step_impl(context, action, acc_name, user):
    sb_id = context.custom_config['sb_user']['sb_id']
    session = context.sb

    if action == 'add':
        acc_type = session.get('https://hrtest-server.sg.com.ua/api/dictionary/platform').json()['values'][0]['id']
        url_create = f'https://hrtest-server.sg.com.ua/api/contact/{sb_id}/accounts'
        result = session.post(
            url=url_create,
            data={"platform": acc_type, "account": acc_name}
        )
        context.account_id = result.json()['id']
    elif action == 'delete':
        url_delete = f'https://hrtest-server.sg.com.ua/api/contact/{sb_id}/accounts/{context.account_id}?delete='
        result = session.post(url=url_delete)
        assert result.status_code

@step("check {action} account {acc_name}-{acc_regex} in reconciliationuserpropaccount table")
def step_impl(context, action, acc_name, acc_regex):
    hr_id = context.custom_config['sb_user']['hr_id']
    user_id = pgsql_select(
        request=f'SELECT * FROM public.index_customuser WHERE hr_id = {hr_id}',
        **context.custom_config['pg_db']
    )[0][0]
    acc_type_id = pgsql_select(
        request=f"SELECT * FROM public.accounting_system_accounttype WHERE account_regexp = '{acc_regex}'",
        **context.custom_config['pg_db']
    )[0][0]
    accounts = pgsql_select(
        request=f'SELECT * FROM public.reconciliation_reconciliationuserpropaccount '
                f'WHERE user_id = {user_id} and account_type_id = {acc_type_id} and month_adj_net is null',
        **context.custom_config['pg_db']
    )

    accounts_id = [acc[0] for acc in accounts]
    session = context.super_user
    for acc_id in accounts_id:
        url = context.custom_config["host"] + f'admin/reconciliation/reconciliationuserpropaccount/{acc_id}/change/'
        text = session.get(url).text
        actual_acc_name = re.findall('<input type="text" name="account" value="([0-9a-zA-Z]*)" class="vTextField', text)[0]
        if actual_acc_name in acc_name:
            assert True if action == "presence" else False
            break
    else:
        assert False if action == "presence" else True

@step("change personal data of user: {user}")
def step_impl(context, user):
    hr_id = context.custom_config['sb_user']['hr_id']
    assert pgsql_update(
        request=f"UPDATE public.index_customuser SET last_name = 'asdasd', first_name = 'asfaf', "
                f"email = 'asd@asd.com', hr_id = 320000, telegram_id = 123123, "
                f"first_work_day = date'1999-01-01' WHERE hr_id = {hr_id}",
        **context.custom_config['pg_db']
    )

@step("check that account(s) == {number} in reconciliationuserpropaccount: {user}")
def step_impl(context, number, user):
    hr_id = context.custom_config['sb_user']['hr_id']
    user_id = pgsql_select(
        request=f'SELECT * FROM public.index_customuser WHERE hr_id = {hr_id}',
        **context.custom_config['pg_db']
    )[0][0]

    accounts = pgsql_select(
        request=f'SELECT * FROM public.reconciliation_reconciliationuserpropaccount '
                f'WHERE user_id = {user_id}',
        **context.custom_config['pg_db']
    )
    assert len(accounts) == int(number)

@step("delete some accounts from reconciliationuserpropaccount: {qty}")
def step_impl(context, qty):
    context.del_accounts = []
    accounts = ReconciliationUserPropaccounts.filter(id__gte=0)
    if qty == 'all':
        for account in accounts:
            if account.month_adj_net != None:
                context.del_accounts.append(account.account)
        accounts.delete()
    elif qty == 'none':
        assert True
    else:
        for i in range(int(qty)):
            if accounts[i].month_adj_net != None:
                context.del_accounts.append(accounts[i].account)
            accounts[i].delete()
    with open('./xxx.txt', 'a') as file:
        file.write(str(context.del_accounts) + '\n')

@step("check group id {group_id} for {param_message}")
@async_run_until_complete
async def step_impl(context, group_id, param_message):
    group = await context.tele_user.get_entity(int(group_id))
    messages = await context.tele_user.get_messages(group, 1)
    message_text = messages[0].message
    with open('./xxx.txt', 'a') as file:
        file.write(str(messages) + '\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(context.del_accounts) + '\n')
    if param_message == 'All accounts from Propreports listed in MSW':
        assert param_message in message_text
    elif param_message == 'Detected non existing in MSW accounts':
        assert param_message in message_text
        for account in context.del_accounts:
            assert account in message_text






import random
import re
from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import correct_py_file
from datetime import date, datetime, timedelta
from base.sql_functions import pgsql_select, pgsql_update
from base.adminka import finish_reconciliation_process
from base.ssh_interaction import change_db_through_django

"""-------------------------------------------MSW-398-------------------------------------"""
@step("get bills id of user 90000")
def step_impl(context):
    context.user_bills = tuple([bill['id'] for bill in context.bills[90000]])

@step("get all transactions of user 90000 {period} reconciliation")
def step_impl(context, period):
    request = f'SELECT * FROM public.accounting_system_transaction ' \
              f'WHERE user_bill_id in {context.user_bills}'
    response = pgsql_select(request, **context.custom_config['pg_db'])
    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(len(response))+'\n')
    if period == "before":
        context.transaction_qty_before = len(response)
    elif period == "after":
        context.transaction_qty_after = len(response)

@step("field -entries created- == {boolean}")
def step_impl(context, boolean):
    request = f"UPDATE public.reconciliation_userdata " \
              f"SET entries_created = '{boolean}' " \
              f"WHERE user_id = 90000"
    assert pgsql_update(request, **context.custom_config['pg_db'])

@step("field -date_reconciliation- == {reconciliation_date}")
def step_impl(context, reconciliation_date):
    if reconciliation_date == "today late":
        rd = datetime.now().replace(hour=23, minute=59, second=59)
        datum = "date '" + str(rd) + "'"
    elif reconciliation_date == "today early":
        rd = datetime.now().replace(hour=0, minute=1,second=59)
        datum = "date '" + str(rd) + "'"
    elif reconciliation_date == "today midday":
        rd = datetime.now().replace(hour=12, minute=0, second=0)
        datum = "date '" + str(rd) + "'"
    elif reconciliation_date == "yesterday":
        rd = datetime.now() - timedelta(days=1)
        datum = "date '" + str(rd) + "'"
    elif reconciliation_date == "tomorrow":
        rd = datetime.now() + timedelta(days=1)
        datum = "date '" + str(rd) + "'"
    elif reconciliation_date == "null":
        datum = 'null'
    request = f"UPDATE public.reconciliation_userdata " \
              f"SET date_reconciliation = {datum} " \
              f"WHERE user_id = 90000"
    assert pgsql_update(request, **context.custom_config['pg_db'])

@step("perform RECONCILIATION")
def step_impl(context):
    finish_reconciliation_process(context, wait_time=20)

@step("compare transactions qty before and after RECONCILIATION {equality}")
def step_impl(context, equality):
    if equality == "true":
        assert context.transaction_qty_before == context.transaction_qty_after
    elif equality == "false":
        assert context.transaction_qty_before != context.transaction_qty_after

@step("field -entries created- should be equal to {result}")
def step_impl(context, result):
    request = f'SELECT * FROM public.reconciliation_userdata ' \
              f'WHERE user_id = 90000'
    response = pgsql_select(request, **context.custom_config['pg_db'])
    assert response[0][21] == eval(result)

"""------------------------------------------------------------------------------------"""
@step("change field -{field}- in UserData table of user with hr_id {hr_id} to {value}")
def step_impl(context, field, hr_id, value):
    old_new_parts={
        '{USER_ID}': hr_id,
        '{FIELD}': field,
        '{VALUE}': value,
    }
    file_name = 'update_userdata'
    file_dir = './base/files_for_ssh'

    correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)


@step("check userdata fields of user 90000 {period} -delete_reconciliation_data-")
def step_impl(context, period):
    fields_list = [
        'zp_cash',
        'podushka',
        'cash',
        'account_plus_minus',
        'social',
        'compensations_total',
        'office_fees',
        'services_total',
        'total_net_month',
        'total_sterling',
        'total_takion',
        'date_reconciliation',
        'qty_of_reconciliations',
        'entries_created',
    ]
    results = []
    for field in fields_list:
        request = f'SELECT {field} FROM public.reconciliation_userdata ' \
                  f'WHERE user_id = 90000'
        response = pgsql_select(request, **context.custom_config['pg_db'])
        results.append(bool(response[0][0]))
    if period == 'before' and True not in results:
        assert False
    elif period == 'after' and True in results:
        assert False

@step("get random account_type: -{acc_group}-")
def step_impl(context, acc_group):
    if acc_group == 'all':
        request = f'SELECT * FROM public.accounting_system_accounttype '
    elif acc_group == 'takion':
        request = f'SELECT * FROM public.accounting_system_accounttype as acct ' \
                  f'JOIN public.accounting_system_broker as accb ON acct.broker_id = accb.id ' \
                  f"WHERE accb.name = 'Takion'"
    elif acc_group == 'sterling':
        request = f'SELECT * FROM public.accounting_system_accounttype as acct ' \
                  f'JOIN public.accounting_system_broker as accb ON acct.broker_id = accb.id ' \
                  f"WHERE accb.name LIKE 'Broker%'"
    response = pgsql_select(request, **context.custom_config['pg_db'])
    acc_type_list = [acc[0] for acc in response]
    context.account_type_id = random.choice(acc_type_list)

@step("create or update user -{hr_id}- propaccount -{acc_name}- with {value}")
def step_impl(context, hr_id, acc_name, value):
    old_new_parts={
        '{USER_ID}': hr_id,
        '{ACC_ID}': str(context.account_type_id),
        '{ACC_NAME}': acc_name,
        '{VALUE}': value,
    }
    file_name = 'update_or_create_propaccount'
    file_dir = './base/files_for_ssh'

    correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("create or update BONUS with {value}")
def step_impl(context, value):
    old_new_parts={
        '{ACC_ID}': str(context.account_type_id),
        '{VALUE}': value,
    }
    file_name = 'update_or_create_bonus'
    file_dir = './base/files_for_ssh'

    correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("BONUS fee of user 90000 should be equal to -{value}-")
def step_impl(context, value):
    request = f'SELECT * FROM public.reconciliation_service ' \
              f'WHERE user_id = 90000'
    response = pgsql_select(request, **context.custom_config['pg_db'])


    session = context.super_user
    url = context.custom_config["host"] + 'admin/reconciliation/service/?q=90000'
    text = session.get(url).text
    if value == 'none':
        asd = re.findall('Bonus</td><td class="field-amount">([0-9/.]*)</td><td class="field-service_type">Fee', text)
        assert len(response) == 0
        assert asd == []
    else:
        asd = re.findall('Bonus</td><td class="field-amount">([0-9/.]*)</td><td class="field-service_type">Fee', text)
        assert len(response) == 1
        assert float(asd[0]) == float(value)

@step("create or update user -{hr_id}- -{serv_type}- with name -{serv_name}-, value -{value}-")
def step_impl(context, hr_id, serv_type, serv_name, value):
    month = datetime.now().month - 1
    serv_date = datetime.now().replace(month=month).timestamp()
    old_new_parts={
        '{USER_ID}': hr_id,
        '{SERV_TYPE}': serv_type,
        '{SERV_NAME}': serv_name,
        '{VALUE}': str(value),
        '{DATE}': str(serv_date)
    }
    file_name = 'update_or_create_service'
    file_dir = './base/files_for_ssh'

    correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("check {field} in UserData table: {first} and {second}")
def step_impl(context, field, first, second):
    request = f'SELECT * FROM public.reconciliation_userdata ' \
              f'WHERE user_id = 90000'
    response = pgsql_select(request, **context.custom_config['pg_db'])
    userdata_id = response[0][0]

    session = context.super_user
    url = context.custom_config["host"] + f'admin/reconciliation/userdata/{userdata_id}/change/'
    text = session.get(url).text

    actual_number = re.findall(f'name="{field}" value="([0-9-]*)" class="vBigIntegerField', text)[0]
    sign = (float(first) + float(second)) / abs(float(first) + float(second))
    expected_number = round(float(first) + float(second) + 0.00000001*sign)

    assert expected_number == int(actual_number)






























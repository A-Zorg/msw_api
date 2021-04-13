import time
import re
from behave import *
from base.main_functions import correct_py_file
from base.sql_functions import pgsql_del, pgsql_select
from base.adminka import task_configuration, run_periodic_task, wait_periodictask_to_be_done
from base.ssh_interaction import change_db_through_django

@step("clear db table: {table}")
def step_impl(context, table):
    request = f"DELETE FROM {table}"
    assert pgsql_del(request, **context.custom_config["pg_db"])

@step("clean db table: {table} where user_id {user_id}")
def step_impl(context, table, user_id):
    request = f"DELETE FROM {table} WHERE user_id = {user_id}"
    assert pgsql_del(request, **context.custom_config["pg_db"])

@step("run the task: {task_name}")
def step_impl(context, task_name):
    session = context.super_user
    task_configuration(session, context.custom_config, task_name)
    assert run_periodic_task(session, context.custom_config)
    # assert run_periodic_task(session=session, task_name=task_name)
    context.start_time = time.time()

@step("upload to the server some file and run it: {file_name}")
def step_impl(context, file_name):
    old_new_parts = {
        '{path}': context.custom_config['server_dir'] + file_name + "_template.xlsx",
        '{path2}': context.custom_config['server_dir'] + file_name + ".xlsx",
    }
    file_dir = './base/files_for_ssh'

    assert correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("modification of msw db to provoke running of bills_corrections by {file_name} - {phrase} - {modificator_types}")
def step_impl(context, file_name, phrase, modificator_types):
    old_new_parts = {
        '{PATH}': context.custom_config['server_dir'] + 'month_propreports_template.xlsx',
        '{PATH2}': context.custom_config['server_dir'] + 'month_propreports.xlsx',
        '{PHRASE}': phrase,
        '{MODIFICATOR_TYPES}': modificator_types,
    }
    file_dir = './base/files_for_ssh'

    assert correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, 'AS_cleaner', file_dir)
    change_db_through_django(context, file_name, file_dir)

@step("get amount of users (90000, 90001) Current Net balance")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + "admin/accounting_system/userbill/"
    response = session.get(url).text

    if context.config.userdata.get("current_net_balance"):
        context.config.userdata["current_net_balance_after_modification"] = re.findall(
            '</a></th><td class="field-bill nowrap">Current Net balance</td><td class="field-amount">([0-9\.-]*)</td></tr>',
            response
        )
        assert context.config.userdata["current_net_balance_after_modification"]
    else:
        context.config.userdata["current_net_balance"] = re.findall(
            '</a></th><td class="field-bill nowrap">Current Net balance</td><td class="field-amount">([0-9\.-]*)</td></tr>',
            response
        )
        assert context.config.userdata["current_net_balance"]

@step("get amounts({qty}) from the monthpropreportstransactios table and check users Current Net balance")
def step_impl(context, qty):
    session = context.super_user
    url = context.custom_config["host"] + "admin/accounting_system/monthpropreportstransaction/"
    response = session.get(url).text
    monthpropreportstransaction_result = re.findall(
        '</td><td class="field-amount">([0-9\.-]*)</td><td',
        response
    )
    suma = lambda amount: round(sum(map(float, amount)), 2)

    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(monthpropreportstransaction_result)+'\n')
    assert int(qty) == len(monthpropreportstransaction_result)
    assert suma(context.config.userdata["current_net_balance_after_modification"]) + suma(monthpropreportstransaction_result) == suma(context.config.userdata["current_net_balance"])


@step("compare sum of Month Adj Net of accounts with Current Net balance sum of users")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + "admin/reconciliation/reconciliationuserpropaccount/"
    response = session.get(url).text

    accounts_amounts = re.findall(
        '</td><td class="field-month_adj_net">([0-9\.-]*)</td></tr>',
        response
    )
    suma = lambda amount: round(sum(map(float, amount)), 2)

    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(suma(accounts_amounts))+'\n')
    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(suma(context.config.userdata["current_net_balance"]))+'\n')

    assert suma(accounts_amounts) == suma(context.config.userdata["current_net_balance"])



@step("wait for task is finished: {task_name}")
def step_impl(context, task_name):
    assert wait_periodictask_to_be_done(task_name, context) == "SUCCESS"
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(time.time()-context.start_time) + '\n')

@step("check that {number} active accounts exist")
def step_impl(context, number):
    request = "SELECT * FROM public.reconciliation_userpropaccount"
    result = pgsql_select(request=request, **context.custom_config['pg_db'])

    if len(result) < 27 * int(number):
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str(context.scenario.skip)+'\n')
        context.scenario.skip(f"accounts qty < {number}")








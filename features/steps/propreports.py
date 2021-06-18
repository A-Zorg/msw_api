import time
import re
import datetime
from behave import *
from base.main_functions import correct_py_file
from base.sql_functions import pgsql_del, pgsql_select, decode_request, encode_request, pgsql_insert
from base.adminka import task_configuration, run_periodic_task, wait_periodictask_to_be_done
from base.ssh_interaction import change_db_through_django, upload_files_server

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

@step("upload to the server some file and run it: {file_name}")
def step_impl(context, file_name):
    old_new_parts = {
        '{path}': context.custom_config['server_dir'] + file_name + "_template.xlsx",
        '{path2}': context.custom_config['server_dir'] + file_name + ".xlsx",
    }
    file_dir = './base/files_for_ssh'

    assert correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)

@step("asdupload to the server some file and run it: {file_name}")
def step_impl(context, file_name):
    old_new_parts = {
        '{path}': context.custom_config['server_dir'] + file_name + "_template.xlsx",
        '{path2}': context.custom_config['server_dir'] + file_name + ".xlsx",
    }
    file_dir = './base/files_for_ssh'

    assert correct_py_file(file_name, old_new_parts)
    change_db_through_django(context, file_name, file_dir)
    from exper import download_from_server
    download_from_server('month_propreports.xlsx')

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
    assert change_db_through_django(context, 'AS_cleaner', file_dir)
    assert change_db_through_django(context, file_name, file_dir)

@step("protoffffffffffffffffffffffffffffffffffffffffffffffffffftype")
def step_impl(context):
    import paramiko
    host = context.custom_config['server']['host']
    port = context.custom_config['server']['port']
    password = context.custom_config['server']['password']
    username = context.custom_config['server']['username']
    with paramiko.Transport((host, int(port))) as transport:
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        remotepath = f'/home/alex_zatushevkiy/msw_api/month_propreports.xlsx'
        localpath = f'C:\\Users\\wsu\\Desktop\\month_propreports.xlsx'
        sftp.put(localpath, remotepath)
        sftp.close()


    file_dir = './base/files_for_ssh'

    assert change_db_through_django(context, 'AS_cleaner', file_dir)
    assert change_db_through_django(context, 'month_propreports_modificator2', file_dir)
@step("hnia")
def step_impl(context):
    from base.db_interactions.reconciliation import ReconciliationUserPropaccounts
    ReconciliationUserPropaccounts.create(
        account='SMRT046N',
        account_type_id=4,
        user_id=713,
        updated=datetime.datetime.now()
    )


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
        '</td><td class="field-amount">([0-9\.-]*)</td>',
        response
    )
    suma = lambda amount: round(sum(map(float, amount)), 2)

    assert "False" not in response
    assert int(qty) == len(monthpropreportstransaction_result)
    assert round((suma(context.config.userdata["current_net_balance_after_modification"]) + suma(monthpropreportstransaction_result)), 2) == suma(context.config.userdata["current_net_balance"])


@step("compare sum of Month Adj Net of accounts with Current Net balance sum of users")
def step_impl(context):
    session = context.super_user
    url = context.custom_config["host"] + "admin/reconciliation/reconciliationuserpropaccount/"
    response = session.get(url).text

    accounts_amounts = re.findall(
        '</td><td class="field-month_adj_net">([0-9\.-]*)</td>',
        response
    )
    while '-' in accounts_amounts:
        accounts_amounts.remove('-')
    suma = lambda amount: round(sum(map(float, amount)), 2)

    assert suma(accounts_amounts) == suma(context.config.userdata["current_net_balance"])

    session = context.super_user
    url = context.custom_config["host"] + "admin/accounting_system/userbill/"
    response = session.get(url).text
    curr_bills = re.findall(
        '</a></th><td class="field-bill nowrap">Current Net balance</td><td class="field-amount">([0-9\.-]*)</td></tr>',
        response
    )
    with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
        file.write(str(curr_bills) + ' asd\n')
    assert suma(accounts_amounts) == suma(curr_bills)




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

@step("migrate user accounts to company")
def step_impl(context):
    request = "SELECT DISTINCT(account),account_type_id " \
              "FROM public.reconciliation_userpropaccount"
    request = decode_request(context, request, ['account'])
    active_accounts = pgsql_select(request=request, **context.custom_config['pg_db'])

    insert_request = "INSERT INTO accounting_system_companypropaccount" \
                     "(account, month_adj_net, account_type_id, updated) " \
                     "VALUES "
    for acc in active_accounts:
        insert_request += f"(=-{acc[0]}-=, =-0-=, {acc[1]}, date('{datetime.datetime.now().date()}')),"
    insert_request = encode_request(context, insert_request)[:-1]
    result = pgsql_insert(request=insert_request, **context.custom_config['pg_db'])

    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(insert_request)+'\n')

@step("compare month_adj_net with sum(daily_adj_net) of company_prop_account")
def step_impl(context):
    request_1 = "SELECT account, SUM(daily_adj_net::float) " \
                "FROM accounting_system_companypropaccountdata " \
                "GROUP BY account "
    request = decode_request(context, request_1, ['account', 'daily_adj_net'])
    result_1 = pgsql_select(request=request, **context.custom_config['pg_db'])

    request_2 = "SELECT account, month_adj_net::float " \
                "FROM accounting_system_companypropaccount "

    request = decode_request(context, request_2, ['account', 'month_adj_net'])
    result_2 = pgsql_select(request=request, **context.custom_config['pg_db'])
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(result_2) + '\n')
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(result_1) + '\n')
    for part in result_1:
        assert part in result_2

@step("check that {number} active accounts of company exist")
def step_impl(context, number):
    request = "SELECT * FROM public.accounting_system_companypropaccountdata"
    result = pgsql_select(request=request, **context.custom_config['pg_db'])

    if len(result) < 27 * int(number):
        with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
            file.write(str(context.scenario.skip)+'\n')
        context.scenario.skip(f"accounts qty < {number}")

@step("amounts from the monthpropreportstransactios table should be {qty}")
def step_impl(context, qty):
    session = context.super_user
    url = context.custom_config["host"] + "admin/accounting_system/monthpropreportstransaction/"
    response = session.get(url).text
    monthpropreportstransaction_result = re.findall(
        '</td><td class="field-amount">([0-9\.-]*)</td>',
        response
    )
    assert int(qty) == len(monthpropreportstransaction_result)

@step("check companybill OPERATIONAL")
def step_impl(context):
    request_bill = "SELECT amount::float " \
                   "FROM accounting_system_companybill " \
                   "WHERE name = 'Operational' "
    request = decode_request(context, request_bill, ['amount'])
    result_bill = pgsql_select(request=request, **context.custom_config['pg_db'])[0][0]

    request_acc = "SELECT SUM(month_adj_net::float) " \
                "FROM accounting_system_companypropaccount "
    request = decode_request(context, request_acc, ['month_adj_net'])
    result_acc = pgsql_select(request=request, **context.custom_config['pg_db'])[0][0]
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(result_bill) + '\n')
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(result_acc) + '\n')
    assert result_bill - result_acc == 10000

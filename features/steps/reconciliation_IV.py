import random
import re
from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import correct_py_file
from datetime import date, datetime, timedelta
from base.sql_functions import pgsql_select, pgsql_update, pgsql_select_as_dict, \
    decode_request, encode_request, pgsql_insert
from base.adminka import finish_reconciliation_process
from base.ssh_interaction import change_db_through_django
from base.db_interactions.accounting_system import PropreportsSubdomain, AccountType, UserBill, UserBillType, HistoryUserBill
from base.db_interactions.reconciliation import ReconciliationUserPropaccounts, PropreportsaccountId, UserData


"""-------------------------------------------MSW-398-------------------------------------"""
@step("get bills id of user 90000")
def step_impl(context):
    context.user_bills = tuple([bill['id'] for bill in context.bills[90000]])

@step("get all transactions of user 90000 {period} reconciliation")
def step_impl(context, period):
    request = f'SELECT * FROM public.accounting_system_transaction ' \
              f'WHERE user_bill_id in {context.user_bills}'
    response = pgsql_select(request, **context.custom_config['pg_db'])

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
    with open('./xxx.txt', 'a') as file:
        file.write(str(context.transaction_qty_before)+'\n')
    with open('./xxx.txt', 'a') as file:
        file.write(str(context.transaction_qty_after)+'\n')
    if equality == "true":
        assert context.transaction_qty_before == context.transaction_qty_after
    elif equality == "false":
        assert context.transaction_qty_before != context.transaction_qty_after

@step("field -entries created- should be equal to {result}")
def step_impl(context, result):
    request = f'SELECT * FROM public.reconciliation_userdata ' \
              f'WHERE user_id = 90000'
    response = pgsql_select(request, **context.custom_config['pg_db'])
    with open('./xxx.txt', 'a') as file:
        file.write(str(response)+'\n')

    assert response[0][8] == eval(result)

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


@step("fields of userdata of user {user_id} should be {answer}")
def step_impl(context, user_id, answer):
    list_fields = [
        'zp_cash',
        'office_fees',
        'podushka',
        'services_total',
        'account_plus_minus',
        'total_net_month',
        'cash',
        'social',
        'date_reconciliation',
        'compensations_total',
    ]
    userdata = UserData.get(user_id=user_id)
    # request = f'SELECT * FROM public.reconciliation_userdata ' \
    #           f'WHERE user_id = {user_id}'
    # response = pgsql_select_as_dict(request, **context.custom_config['pg_db'])
    # userdata = response[0]

    if answer == 'none':
        for field in list_fields:
            assert getattr(userdata, field) == None
        assert getattr(userdata, 'entries_created') == False
        assert getattr(userdata, 'qty_of_reconciliations') == 0
    elif answer == 'not none':
        check_list = []
        for field in list_fields:
            check_list.append(getattr(userdata, field) != None)
        with open('./xxx.txt', 'a') as file:
            file.write(str(check_list) + '\n')
        assert any(check_list)
        # assert userdata['entries_created'] == True
        assert getattr(userdata, 'qty_of_reconciliations') != 0

# @step("get bills: {bills} of user {user_id}")
# def step_impl(context, bills, user_id):
#     bills_list = bills.split(',')
#     # request = f'SELECT id, bill_id FROM accounting_system_userbill ' \
#     #           f'WHERE user_id = {user_id} and bill_id in (' \
#     #           f'SELECT id FROM accounting_system_userbilltypes ' \
#     #           f'WHERE name in ({bills}))'
#     # response = pgsql_select_as_dict(request, **context.custom_config['pg_db'])
#     # context.user_bills = response
#     bill_types = UserBillType.filter(name__in=['Account', 'Current Net balance'])
#     context.bills = UserBill.filter(user_id=user_id, bill_id__in=bill_types)
#     with open('./xxx.txt', 'a') as file:
#         file.write(str(bill_types) + '\n')
#     with open('./xxx.txt', 'a') as file:
#         file.write(str(context.bills ) + '\n')

@step("create the set of history_user_bill of user {user_id}")
def step_impl(context, user_id):
    curc_month = datetime.now().replace(day=1, hour=23, minute=59)
    prev_month = curc_month - timedelta(days=1)
    prevprev_month = prev_month.replace(day=1) - timedelta(days=1)

    context.exp_result = {
        "account": 555.0,
        "prev_month_net": 623.0,
    }

    current_net_bal = UserBill.get(user_id=user_id, bill_id__name='Current Net balance')
    account = UserBill.get(user_id=user_id, bill_id__name='Account')

    new_history_models = [
        {
            'model_id': current_net_bal.id,
            'history_date': prevprev_month,
            'history_created': datetime.now(),
            'history_type': '~',
            'amount': context.exp_result['prev_month_net'],
            'bill_id': current_net_bal.bill_id,
            'user_id': user_id
        },
        {
            'model_id': current_net_bal.id,
            'history_date': prevprev_month.replace(day=27),
            'history_created': datetime.now(),
            'history_type': '~',
            'amount': 456,
            'bill_id': current_net_bal.bill_id,
            'user_id': user_id
        },
        {
            'model_id': account.id,
            'history_date': prev_month,
            'history_created': datetime.now(),
            'history_type': '~',
            'amount': context.exp_result['account'],
            'bill_id': account.bill_id,
            'user_id': user_id
        },
        {
            'model_id': account.id,
            'history_date': curc_month,
            'history_created': datetime.now(),
            'history_type': '~',
            'amount': 444,
            'bill_id': account.bill_id,
            'user_id': user_id
        },
    ]
    for part in new_history_models:
        HistoryUserBill.create(**part)

@step("compare actual with expected fields: account and prev_month_net of user {user_id}")
def step_impl(context, user_id):
    userdata = UserData.get(user_id=user_id)

    for key in context.exp_result:
        assert context.exp_result[key] == getattr(userdata, key)

@step("check custom_podushka of user {user_id} (should be {answer})")
def step_impl(context, user_id, answer):
    request = f'SELECT custom_podushka FROM reconciliation_userdata ' \
              f'WHERE user_id = {user_id}'
    response = pgsql_select(request, **context.custom_config['pg_db'])[0]
    assert str(response[0]) == answer


@step("get expected [RC] tasks(qty:{number})")
def step_impl(context, number):

    recon_date = datetime.now() + timedelta(hours=48)
    rec_day = recon_date.day
    rec_month = recon_date.month
    context.expected_pertasks = [
        [
            '[RC] StartReconciliation',
            'auto_start_reconciliation',
            0, 10, rec_day, rec_month
        ],
        # [
        #     '[RC] StartReconciliationUpdates - Check for non-existing accounts',
        #     'check_for_non_existent_prop_accounts_monthly',
        #     30, 10, rec_day - 1, rec_month
        # ],
        [
            '[RC] StartReconciliationUpdates - Create Bonus Fees',
            'create_bonus_fees',
            0, 10, rec_day-1, rec_month
        ],
        [
            '[RC] StartReconciliationUpdates - PropreportsMonthCorrections',
            'entries_for_prop_month_correction',
            0, 10, rec_day-1, rec_month
        ],
        [
            '[RC] StartReconciliationUpdates - Services & Compensations',
            'import_services_and_compensations',
            50, 9, rec_day-1, rec_month
        ],
        [
            '[RC] StartReconciliationUpdates - Propreports import files',
            'download_from_propreports_monthly',
            5, 8, rec_day-1, rec_month
        ],
        [
            '[RC] StartReconciliationUpdates - HR Module',
            'import_HR_module',
            0, 8, rec_day-1, rec_month
        ],
        [
            '[RC] StartReconciliationUpdates - Delete old reconciliation data',
            'delete_reconciliation_data',
            0, 8, rec_day-1, rec_month
        ],
        [
            '[RC] TransferBillsToReconciliation',
            'transfer_bills_to_reconciliation',
            0, 8, rec_day-1, rec_month
        ],
    ]

@step("get actual [RC] tasks(qty:{number})")
def step_impl(context, number):
    request = f'SELECT name, task, minute::int, hour::int::int::int, day_of_month::int::int, month_of_year::int ' \
              f'FROM django_celery_beat_periodictask as p ' \
              f'JOIN django_celery_beat_crontabschedule as c ON p.crontab_id = c.id ' \
              f'ORDER BY p.id DESC LIMIT {number}'

    response = pgsql_select(request, **context.custom_config['pg_db'])

    context.actual_pertasks = [list(task) for task in response]
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.actual_pertasks) + '\n')

@step("compare expected and actual [RC] tasks")
def step_impl(context):
    assert context.actual_pertasks == context.expected_pertasks


@step("[services]get total_{field_type} of user {user_id}")
def step_impl(context, field_type, user_id):
    request = f"SELECT SUM(amount::float) FROM public.reconciliation_service " \
              f"WHERE user_id = {user_id} and service_type='{field_type}'"

    # request = decode_request(context, request, ['amount'])
    response = pgsql_select(request, **context.custom_config['pg_db'])[0][0]

    if hasattr(context, 'expected_total'):
        context.expected_total[field_type] = round(response) if response else 0
    else:
        context.expected_total = {}
        context.expected_total[field_type] = round(response) if response else 0

@step("[account]get total_{field_type} of user {user_id}")
def step_impl(context, field_type, user_id):
    request = f"SELECT SUM(month_adj_net::float) FROM reconciliation_reconciliationuserpropaccount as acr " \
              f"JOIN accounting_system_accounttype as act ON acr.account_type_id=act.id " \
              f"JOIN accounting_system_broker as acb ON act.broker_id=acb.id " \
              f"WHERE acr.user_id = {user_id} and acb.name like '%{field_type}%'"

    # request = decode_request(context, request, ['month_adj_net'])
    response = pgsql_select(request, **context.custom_config['pg_db'])[0][0]

    if hasattr(context, 'expected_total'):
        context.expected_total[field_type.lower()] = round(response) if response else 0
    else:
        context.expected_total = {}
        context.expected_total[field_type.lower()] = round(response) if response else 0

@step("get user_totals from UserData of user {user_id}")
def step_impl(context, user_id):
    request = f"SELECT prev_month_net::float as prev_month, compensations_total::float as compensation, " \
              f"services_total::float as service, office_fees::float as fee, total_net_month::float as total_net, " \
              f"total_sterling::float as Broker, total_takion::float as Takion " \
              f"FROM public.reconciliation_userdata " \
              f"WHERE user_id = {user_id}"

    # request = decode_request(
    #     context,
    #     request,
    #     [
    #         'prev_month_net',
    #         'compensations_total',
    #         'services_total',
    #         'office_fees',
    #         'total_net_month',
    #         'total_sterling',
    #         'total_takion',
    #     ]
    # )
    context.actual_total = dict(pgsql_select_as_dict(request, **context.custom_config['pg_db'])[0])

@step("compare actual_total with expected_total")
def step_impl(context):
    context.expected_total['total_net'] = context.actual_total['prev_month'] \
                                          + context.expected_total['takion'] \
                                          + context.expected_total['broker'] \
                                          + context.expected_total['compensation'] \
                                          + context.expected_total['service']
    del context.actual_total['prev_month']
    assert context.actual_total == context.expected_total

@step("get {hr_id} user's accounts which belong to subdomain {subdomain} through {source}")
def step_impl(context, hr_id, subdomain, source):
    if source == 'api':
        session = context.super_user
        url = context.custom_config["host"] + f'api/reconciliation/accounts/{hr_id}/{subdomain}/'
        result = session.get(url).json()
        context.api_accounts = [part['account'] for part in result]
    elif source == 'db':
        account_types = AccountType.filter(propreports_subdomain_id__subdomain=subdomain)
        result = ReconciliationUserPropaccounts.filter(
            user_id__hr_id=hr_id,
            account_type_id__in=account_types
        )
        context.api_accounts = [part.account for part in result]

@step("get to these accounts propreports_id and group_id through {source}")
def step_impl(context, source):
    if source == 'api':
        session = context.super_user
        url = context.custom_config["host"] + 'api/reconciliation/accounts/propreports/{0}/'
        context.api_result = {}
        for account in context.api_accounts:
            ''.format()
            response = session.get(url.format(account)).json()
            context.api_result[account] = response
    elif source == 'db':
        sql_response = PropreportsaccountId.filter(account__in=context.api_accounts)
        context.db_result = {}
        for part in sql_response:
            context.db_result[part.account] = {
                'propreports_id': part.propreports_id,
                'group_id': part.group_id
            }

@step("compare data from db and api")
def step_impl(context):
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.db_result) + '\n')
    # with open('./xxx.txt', 'a') as file:
    #     file.write(str(context.api_result) + '\n')
    assert context.db_result == context.api_result




















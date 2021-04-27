import re
import time
import datetime
import requests
import pyotp
import pandas
from base.sql_functions import pgsql_select, pgsql_insert, pgsql_del


def get_token(session, url, key='csrftoken'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = session.get(url, headers=headers)
    if key == 'csrftoken':
        token = re.findall('name="csrfmiddlewaretoken" value="([a-zA-Z0-9]*)">', html.text)[0]
    elif key == 'X-CSRFToken':
        token = re.findall('csrfToken: "([a-zA-Z0-9]*)"', html.text)[0]
    return token

def create_user_session(host, username, password, totp):
    """creat session in admin"""
    start = f'{host}admin/'
    end = f'{host}admin/login/?next=/admin/'
    session = requests.Session()
    totp_code = pyotp.TOTP(totp)

    session.get(start)
    request_dict = {'username': username, 'password': password, 'next': '/admin/'}
    request_dict['csrfmiddlewaretoken'] = session.cookies['csrftoken']
    request_dict['otp_token'] = totp_code.now()

    response = session.post(end, data=request_dict, headers={"Referer": end})

    if "Welcome" in response.text:
        print(f'{username} was login')
    else:
        raise Exception(f'{username} was not login')

    return session


def task_configuration(session, config, regtask, arg=[], kwarg={}):
    """make reconciliation active"""
    url = f'{config["host"]}admin/django_celery_beat/periodictask/{config["periodic_task"]}/change/'
    token = get_token(session, url)

    recon_dict = {
        'csrfmiddlewaretoken': token,
        'name': 'xxx',
        'regtask' : regtask,
        'task': '',
        'description': '',
        'interval': '1',
        'args': str(arg).replace('\'', '"'),
        'kwargs': str(kwarg).replace('\'', '"'),
        'expires_0': '',
        'expires_1': '',
        'expire_seconds': '',
        'queue': '',
        'exchange': '',
        'routing_key': '',
        'priority': '',
        'headers': '{}',
        '_save': 'Save',
    }
    response = session.post(url, data=recon_dict, headers={"Referer": url})
    return response.ok

def run_periodic_task(session, config):
    """run periodic task"""
    url = config["host"] + 'admin/django_celery_beat/periodictask/'
    token = get_token(session, url)
    task_id = config["periodic_task"]

    recon_dict = {
        'csrfmiddlewaretoken': token,
        'action': 'run_tasks',
        'select_across': '0',
        'index': '0',
        '_selected_action': task_id,
    }
    response = session.post(url, data=recon_dict, headers={"Referer": url})

    return response.ok

def start_reconciliation(session, host, number=1):
    """make reconciliation active"""
    from datetime import date, timedelta
    url = f'{host}admin/reconciliation/statusreconciliation/{number}/change/'

    get = session.get(url)
    csrfmiddlewaretoken = re.findall('name="csrfmiddlewaretoken" value="(.+)">', get.text)[0]

    date_activated_0 = date.today() - timedelta(3)
    date_stopped_0 = date.today() + timedelta(1)

    recon_dict = {
        'csrfmiddlewaretoken' : csrfmiddlewaretoken,
        'status': 'on',
        'date_activated_0': date_activated_0,
        'date_activated_1': '16:18:47',
        'date_stopped_0': date_stopped_0,
        'date_stopped_1': '16:18:47',
        '_save': 'Save',
    }

    session.post(url, data=recon_dict, headers={"Referer": url})

def wait_periodictask_to_be_done(task_name, context, wait_time=3600):
    """
    wait for some periodic task to be done
    take = name of the task
    return task_state
    after 10 min - exit from function if task would not be done
    """
    request = "SELECT * FROM public.django_celery_results_taskresult ORDER BY id DESC "
    start_id = pgsql_select(request=request, **context.custom_config['pg_db'])[0][0]

    start_time = time.time()
    while (time.time() - start_time) < wait_time:
        request = 'SELECT * FROM public.django_celery_results_taskresult ' \
                  f'WHERE id > {start_id} and task_name=\'{task_name}\'' \
                  'ORDER BY id ASC '
        result = pgsql_select(request=request, **context.custom_config['pg_db'])

        if result:
            return result[0][2]
        time.sleep(10)
    return "FAILURE"

def check_users_presence(session, config):
    """check of test users"""
    url = config["host"] + 'admin/index/customuser/90000/change/'
    response = session.get(url)
    return '90000' in response.text


def finish_reconciliation_process(context, wait_time=1200):
    session = context.super_user
    start_reconciliation(session=session, host=context.custom_config["host"])
    task_configuration(session, context.custom_config, "auto_stop_reconciliation")
    run_periodic_task(session, context.custom_config)
    result = wait_periodictask_to_be_done(
        task_name="create_and_apply_all_reconciliation_entries",
        context=context,
        wait_time=wait_time
    )

    if result == "FAILURE":
        raise Exception
    else:
        print("reconciliation was finished")

def dr_dataset_uploader(db_creds, date_list, reviewed_days=2):
    """
    upoload dataset for DR for dates which are in date_list
    """
    dataset = pandas.read_csv('./generator/dataset_dr.csv')
    for i in range(reviewed_days):
        fields = ', '.join(dataset.columns[1:])
        request_template = f'INSERT INTO public.review_propreportsdata({fields}) VALUES '
        request = request_template
        for index, row in dataset.iterrows():
            row['review_date'] = date_list[1+i]
            if datetime.time.fromisoformat(row['execution_time']) >= datetime.time(10, 0, 0):
                row['execution_date'] = date_list[0+i]
            else:
                row['execution_date'] = date_list[1+i]
            unit = list(row)
            unit[11] = unit[12] = unit[13] = 0
            unit = str(unit[1:])
            request = request + '(' + unit[1:-1] + '),'

            if index % 5000 == 0:
                pgsql_insert(request[:-1], **db_creds)
                request = request_template
        response = pgsql_insert(request[:-1], **db_creds)
        assert response

def calculation_starter(context, date_list, days=2):
    """
    run task 'start_session_calculations' for dates which are in date_list
    """
    session = context.super_user
    interaction_dict = {
        "INT": "update_postmarket_unrealized",
        "PRE": "start_session_calculations",
    }

    for i in range(days):
        working_date = date_list[1+i]
        for key, value in interaction_dict.items():
            task_configuration(
                session=session,
                config=context.custom_config,
                regtask='start_session_calculations',
                arg=f'["{key}", "{working_date}"]'
            )

            print(f'["{key}", "{str(working_date)}"]')
            run_periodic_task(
                session=session,
                config=context.custom_config,
            )
            result = wait_periodictask_to_be_done(task_name=value, context=context)
            print(result)

def perform_dr_calculation(context, calculation_date):
    """
    Perform DR calculation for chosen date
    :param context: Behave context
    :param calculation_date: chosen date
    :return:
    """
    target_date = datetime.datetime.fromisoformat(calculation_date)
    target_date_week_day = target_date.weekday()

    if target_date_week_day in [5, 6]:
        target_date = target_date + datetime.timedelta(days=2)
        target_date_week_day = target_date.weekday()
        print("DR date is not business day, so it was changed to another")

    if target_date_week_day == 0:
        prev_date = target_date - datetime.timedelta(days=3)
        next_date = target_date + datetime.timedelta(days=1)
    elif target_date_week_day == 4:
        prev_date = target_date - datetime.timedelta(days=1)
        next_date = target_date + datetime.timedelta(days=3)
    else:
        prev_date = target_date - datetime.timedelta(days=1)
        next_date = target_date + datetime.timedelta(days=1)

    context.dr_dates = {
        "prev_date": str(prev_date.date()),
        "target_date": str(target_date.date()),
        "next_date": str(next_date.date())
    }
    # for cleared_date in context.dr_dates.values():
    #     request = "DELETE FROM public.review_propreportsdata " \
    #               f"WHERE review_date = date'{cleared_date}'"
    #     assert pgsql_del(request, **context.custom_config['pg_db'])
    #
    # dr_dataset_uploader(
    #     db_creds=context.custom_config['pg_db'],
    #     date_list=list(context.dr_dates.values())
    # )
    # calculation_starter(
    #     context=context,
    #     date_list=list(context.dr_dates.values())
    # )
    print('DR_dataset is uploaded')


def wait_periodictask_to_be_done2(task_name, pgsql, wait_time=3600):
    """
    wait for some periodic task to be done
    take = name of the task
    return task_state
    after 10 min - exit from function if task would not be done
    """
    request = "SELECT * FROM public.django_celery_results_taskresult ORDER BY id DESC "
    start_id = pgsql_select(request=request, **pgsql)[0][0]

    start_time = time.time()
    while (time.time() - start_time) < wait_time:
        request = 'SELECT * FROM public.django_celery_results_taskresult ' \
                  f'WHERE id > {start_id} and task_name=\'{task_name}\'' \
                  'ORDER BY id ASC '
        result = pgsql_select(request=request, **pgsql)

        if result:
            return result[0][2]
    return "FAILURE"


















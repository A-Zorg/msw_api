import re
import time
import requests
import pyotp
from base.sql_functions import pgsql_select


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
        'args': str(arg),
        'kwargs': str(kwarg),
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


















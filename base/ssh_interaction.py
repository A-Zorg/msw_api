import paramiko
import requests
import pyotp
from datetime import date, timedelta
import re
import time

def loader(host,user,secret,port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)

    stdin, stdout, stderr = client.exec_command('cd /smartteam/msw_server_9999/msw && python3 manage.py shell < /home/alex_zatushevkiy/3/loader.py')
    client.close()
    time.sleep(25)
def cleaner(host,user,secret,port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)

    stdin, stdout, stderr = client.exec_command('cd /smartteam/msw_server_9999/msw && python3 manage.py shell < /home/alex_zatushevkiy/3/cleaner.py')
    client.close()

def create_user_session(username, password, totp):
    start = 'https://mytest-server.sg.com.ua:9999/admin/'
    end = 'https://mytest-server.sg.com.ua:9999/admin/login/?next=/admin/'
    session = requests.Session()
    totp_code = pyotp.TOTP(totp)

    session.get(start)
    request_dict = {'username': username, 'password': password, 'next': '/admin/'}
    request_dict['csrfmiddlewaretoken'] = session.cookies['csrftoken']
    request_dict['otp_token'] = totp_code.now()
    session.post(end, data=request_dict, headers={"Referer": end})
    return session

def start_reconciliation(data):
    session = create_user_session(**data)
    url = 'https://mytest-server.sg.com.ua:9999/admin/reconciliation/statusreconciliation/1/change/'

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
    session.close()
    time.sleep(30)
def stop_reconciliation(data):
    session = create_user_session(**data)
    url = 'https://mytest-server.sg.com.ua:9999/admin/django_celery_beat/periodictask/'

    get = session.get(url)
    csrfmiddlewaretoken = re.findall('name="csrfmiddlewaretoken" value="(.+)">', get.text)[0]

    recon_dict = {
        'csrfmiddlewaretoken' : csrfmiddlewaretoken,
        'action': 'run_tasks',
        'select_across': '0',
        'index': '0',
        '_selected_action': '6',
    }

    session.post(url, data=recon_dict, headers={"Referer": url})
    session.close()
    time.sleep(10)
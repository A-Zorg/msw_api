import configparser
import re
from base.adminka import create_user_session, wait_periodictask_to_be_done2
import paramiko
import time
import datetime

config = configparser.ConfigParser()
config.read("cred/config.ini")
#
# host = config['server']['host']
# port = int(config['server']['port'])
# user = config['server']['username']
# password = config['server']['password']
# """----------------------upload excel file---------------------------"""
# transport = paramiko.Transport((host, port))
# transport.connect(username=user, password=password)
# sftp = paramiko.SFTPClient.from_transport(transport)
#
#
# remotepath = f'/home/alex_zatushevkiy/month_import/accounts.xlsx'
# localpath = f'C:/Users/wsu/Desktop/accounts.xlsx'
# sftp.put(localpath, remotepath)
#
# sftp.close()
# transport.close()
# time.sleep(10)
#
# """---------------------run script on server-------------------"""
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(hostname=host, username=user, password=password, port=port)
#
# stdin, stdout, stderr = client.exec_command('cd /smartteam/msw_server_9999/msw && '
#                                             'python3 manage.py shell < /home/alex_zatushevkiy/10/cleaner_super.py && '
#                                             'python3 manage.py shell < /home/alex_zatushevkiy/month_import/poo.py')
# client.close()
# time.sleep(15)
"""------------------------------run month import---------------------------------"""
# session = create_user_session(config['host']['host_9999'], **config['super_user_9999'])
#
# for i in range(1):
#     url = f'https://mytest-server.sg.com.ua:9999/api/accounting_system/full_prop_data/' \
#           f'?date_from=2021-06-25&file_format=xlsx'
#
#     a = time.time()
#     get = session.get(url)
#     print(get.status_code)
#     print(time.time() - a)
#     # print(get.text)
#     # print(len(get.json()))
#     with open(f'./as45_report.xlsx', 'wb') as file:
#         file.write(get.content)
#     print(time.time() - a)

# csrfmiddlewaretoken = re.findall('name="csrfmiddlewaretoken" value="(.+)">', get.text)[0]
#
# recon_dict = {
#         'csrfmiddlewaretoken' : csrfmiddlewaretoken,
#         'action': 'run_tasks',
#         'select_across': '0',
#         'index': '0',
#         '_selected_action': '86',
#     }
# print(datetime.datetime.now())
# session.post(url, data=recon_dict, headers={"Referer": url})
# print(datetime.datetime.now())
# asd = config["pg_db_9999"]
#
# print(wait_periodictask_to_be_done2('import_from_propreports_monthly', asd))
# print(datetime.datetime.now())
#
# print(wait_periodictask_to_be_done2('entries_for_prop_month_correction', asd))
# print(datetime.datetime.now())



from  base.main_functions import get_token
# session = create_user_session(config['host']['host_9999'], **config['super_user_9999'])
# for i in range(3):
#     url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
#     request = {
#         'transaction_out.user_bill': '142015',
#         'transaction_out.company_bill': '',
#         'transaction_in.user_bill': '',
#         'transaction_in.company_bill': '120',
#         'entry.date_to_execute': '2021-08-10T00:00:00',
#         'entry.description': 'autotest',
#         'transaction_common.amount_usd': '9',
#         'transaction_common.description': 'autotest',
#         'csrfmiddlewaretoken': get_token(session, url),
#     }
#     response = session.post(url, data=request, headers={"Referer": url})
#     print(response.text)
#     entry = response.json()['entry']
#     time.sleep(0.1)
    # url = f'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/cancel/{entry}/'
    # response = session.get(url)
    # print(response.text)

import requests


# url = 'https://mytest-server.sg.com.ua:9999/api/token/'
# session = requests.Session()
#
# request_dict = {
#     'username': 'Admin_Zatush',
#     'password': '1423qrwe',
# }
# response = session.post(url, data=request_dict)
# tokens = response.json()
# access = tokens['access']
# print('access token: ', access)
#
#
#
# url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/app/full_prop_data/'
#
# token2 = get_token(session, url, key ='X-CSRFToken')
#
# url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/app/full_prop_data/'
# resp = session.get(url, headers={"Authorization": f'Token {access}'})
# # print(resp.request.headers)
# print(resp.status_code)
# print(resp.text)

url = "https://test.pinesoftware.com.cy:9443/contacts/"
session = requests.Session()
token = get_token(session, url)
body = {
    'csrfmiddlewaretoken': token,
    'first_name': 'asdasdsdg',
    'last_name': 'fjfgj',
    'email': 'asd@gmail.com',
    'telephone': '+56784938456',
    'text': 'asdgasdgasdg',
    'contacts': '',
    'file': '',
}
response = session.post(url, data=body, headers={"Referer": url})

print(response.text)
print(response.status_code)









import configparser
import re
from base.ssh_interaction import create_user_session
import paramiko
import time

config = configparser.ConfigParser()
config.read("cred/config.ini")

host = config['server']['host']
port = int(config['server']['port'])
user = config['server']['user']
password = config['server']['secret']
"""----------------------upload excel file---------------------------"""
transport = paramiko.Transport((host, port))
transport.connect(username=user, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)


remotepath = f'/home/alex_zatushevkiy/month_import/accounts.xlsx'
localpath = f'C:/Users/wsu/Desktop/accounts.xlsx'
sftp.put(localpath, remotepath)

sftp.close()
transport.close()
time.sleep(10)

"""---------------------run script on server-------------------"""
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, port=port)

stdin, stdout, stderr = client.exec_command('cd /smartteam/msw_server_9999/msw && '
                                            'python3 manage.py shell < /home/alex_zatushevkiy/10/cleaner_super.py && '
                                            'python3 manage.py shell < /home/alex_zatushevkiy/month_import/poo.py')
client.close()
time.sleep(5)
"""------------------------------run month import---------------------------------"""
# session = create_user_session(**config['super_user'])
# url = 'https://mytest-server.sg.com.ua:9999/admin/django_celery_beat/periodictask/'
#
# get = session.get(url)
# csrfmiddlewaretoken = re.findall('name="csrfmiddlewaretoken" value="(.+)">', get.text)[0]
#
# recon_dict = {
#         'csrfmiddlewaretoken' : csrfmiddlewaretoken,
#         'action': 'run_tasks',
#         'select_across': '0',
#         'index': '0',
#         '_selected_action': '86',
#     }
#
# session.post(url, data=recon_dict, headers={"Referer": url})
# time.sleep(5)
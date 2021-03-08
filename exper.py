from allure_behave.hooks import allure_report
import configparser
from datetime import datetime, timedelta
import re
import pandas as pd
import requests
from base.ssh_interaction import create_user_session
from base.main_functions import get_token
import paramiko
import requests
import time
import random

# config = configparser.ConfigParser()
# config.read("cred/config.ini")
# host = config['server']['host']
# port = int(config['server']['port'])
# user = config['server']['user']
# password = config['server']['secret']
# """----------------------upload excel file---------------------------"""
# transport = paramiko.Transport((host, port))
# transport.connect(username=user, password=password)
# sftp = paramiko.SFTPClient.from_transport(transport)
#
#
# remotepath = f'/home/alex_zatushevkiy/3/loader.py'
# localpath = f'C:/Users/wsu/Desktop/loader222.py'
# sftp.get(remotepath, localpath)
#
# sftp.close()
# transport.close()

# """---------------------------------------------------------------"""
# session = create_user_session(**config['manager_user'])
# url = 'https://mytest-server.sg.com.ua:9999/api/reconciliation/'
#
# get = session.get(url)
# print(get.text)
# # csrfmiddlewaretoken = re.findall('name="csrfmiddlewaretoken" value="(.+)">', get.text)[0]
# #
# # recon_dict = {
# #         'csrfmiddlewaretoken' : csrfmiddlewaretoken,
# #         'action': 'run_tasks',
# #         'select_across': '0',
# #         'index': '0',
# #         '_selected_action': '86',
# #     }
# #
# # session.post(url, data=recon_dict, headers={"Referer": url})
# time.sleep(5)

# import py7zr
#
# with py7zr.SevenZipFile('C:/Users/wsu/Desktop/ac.7z', 'w', password='123456') as archive:
#     archive.writeall('C:/Users/wsu/Desktop/3/users.csv', 'users.csv',)



# from openpyxl import Workbook
# from openpyxl import load_workbook
#
#
# wb1 = load_workbook('C:/Users/wsu/Desktop/3/fees.xlsx')
# ws1 = wb1.active
# wb2 = load_workbook('C:/Users/wsu/Desktop/december.xlsx')
# ws2 = wb2.active
#
# from_file = ws1['D2':'H4']
# to_file = ws2['K5':'O7']
# for i in range(len(to_file)):
#     for j in range(len(to_file[i])):
#         to_file[i][j].value=from_file[i][j].value
# wb2.save('C:/Users/wsu/Desktop/dec.xlsx')

from base64 import b64decode
import io

# sess = context.manager_user
# asd = sess.get('https://mytest-server.sg.com.ua:9999/api/media/contest/smartheat/image')
# bb= eval(asd.text)['image'].split(',')
# print(bb)
# cc = b64decode(bb[1])
# with open('C:\\Users\\wsu\\Desktop\\xx.jpg', 'rb') as file:
#     a=file.read()
#     print(type(a))
#     dataa = io.BytesIO()
#     dataa.write(a)
#     print(type(dataa))

    # a_byte_array = bytearray(bb['image'], "utf8")
    # print(a_byte_array)
    # # byte_list = []
    # # for byte in a_byte_array:
    # #     binary_representation = bin(byte)
    # #     byte_list.append(binary_representation)
    # with open('C:\\Users\\wsu\\Desktop\\xx.jpg','wb') as file:
    #     file.write(cc)


# session = create_user_session(**config['fin_user'])

# user_bills = [i['id'] for i in session.get('https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/users/').json() if i['user']>=90000 and i['user']<=90500]
# company_bills = [i['id'] for i in session.get('https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/').json()]
# url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
# print(user_bills)
# for i in range(100):
#     token = get_token(session, url)
#     exec_date = datetime.now().replace(day=random.randint(1,28), second=0, microsecond=0)
#     request_dict ={
#                            'transaction_out.user_bill': '',
#                            'transaction_out.company_bill': random.choice(company_bills),
#                            'transaction_in.user_bill': random.choice(user_bills),
#                            'transaction_in.company_bill': '',
#                            'entry.date_to_execute': exec_date.__str__().replace(' ', 'T'),
#                            'entry.description': '',
#                            'transaction_common.amount_usd': random.randint(-50, 50),
#                            'transaction_common.description': '',
#                            'csrfmiddlewaretoken': token,
#     }
#     response = session.post(url, data=request_dict, headers={"Referer": url})
#     print(response.status_code)


# start = time.time()
# url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entries/?user[]=all&account[]=all&date_from=2021-02-19T00:00:00&date_to=2021-03-10T00:00:00'
# with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
#     file.write(f'url - {url}'+ '\n')
# # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
# #         file.write('Start of the requests: '+str(start) + '\n')
# resp = session.get(url)
# print(resp.status_code)
# print(resp.text)
# print(time.time()-start)
# with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
#     file.write('status code of the request: ' + str(resp.status_code) + '\n')
# with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
#     file.write('amount of entries: ' + str(len(resp.json())) + '\n')
# with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
#     file.write('Time of the requests: ' + str(time.time()-start) + '\n')
# with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
#     file.write('______________________________________________________________' + '\n')
#



# def run():
#     import sys
#     f1 = sys.stdin
#     f = open('input.txt','r')
#     sys.stdin = f
#     a = input("name: ")
#     print(a)
#     f.close()
#     sys.stdin = f1
#
# run()
#
# import sys
#
# for line in sys.stdin:
#     if 'q' == line.rstrip():
#         break
#     print(f'Input : {line}')
#
# print("Exit")
#
# import os
# from zipfile import ZipFile
#
#
# try:
#     bot_name = os.environ['BOT_NAME']
# except:
#     bot_name = "sasa"

# request_head = {"PRIVATE-TOKEN": "BWwoAwHkq8qr1gs8QMHr"}
# url = "https://gitlab.com/api/v4/projects/24782639/jobs"
# response = requests.get(url, headers=request_head)
# job_list = response.json()
#
# for job in job_list:
#     job_id = job['id']
#     job_name = job['name']
#     job_stage = job['stage']
#     # print(job_id)
#     if job_name == "pages" and job_stage == "deploy":
#         request_head = {"PRIVATE-TOKEN": "BWwoAwHkq8qr1gs8QMHr"}
#         url = f"https://gitlab.com/api/v4/projects/24782639/jobs/{job_id}/artifacts"
#         response = requests.get(url, headers=request_head)
#
#         with open('./art.zip','wb') as file:
#             file.write(response.content)
#
#         with ZipFile('./art.zip') as myzip:
#             with myzip.open('public/widgets/summary.json') as myfile:
#                 bot_nickname = eval(myfile.read())["reportName"]
#                 if bot_name == bot_nickname:
#                     myzip.extractall()
#                     break
# with open('./public/widgets/summary.json', 'r') as file:
#     data = str(file.read())
# with open('./public/widgets/summary.json', 'w') as file:
#     file.write(data.replace('Allure Report', bot_name))

#
# sess = requests.Session()
# request_head = {"PRIVATE-TOKEN": "BWwoAwHkq8qr1gs8QMHr"}
# url = "https://gitlab.com/api/v4/projects/24782639/jobs/1076995374/artifacts"
# response = sess.get(url, headers=request_head)
# print(response.status_code)
#
# url = "https://gitlab.com/api/v4/projects/24782639/jobs/1076995374/artifacts"
# response = sess.get(url, headers=request_head)
# print(response.status_code)
# with open('./art.zip', 'wb') as file:
#     file.write(response.content)


import os
from zipfile import ZipFile
import requests


def past_report(bot_name):
    """download past report of some bot"""

    request_head = {"PRIVATE-TOKEN": "BWwoAwHkq8qr1gs8QMHr"}
    url = "https://gitlab.com/api/v4/projects/24782639/jobs"
    response = requests.get(url, headers=request_head)
    job_list = response.json()
    print(response.status_code)

    for job in job_list:
        job_id = job['id']
        job_name = job['name']
        job_stage = job['stage']

        if job_name == "pages" and job_stage == "deploy":
            request_head = {"PRIVATE-TOKEN": "BWwoAwHkq8qr1gs8QMHr"}
            url = "https://gitlab.com/api/v4/projects/24782639/jobs/{}/artifacts".format(job_id)
            print(url)
            response = requests.get(url, headers=request_head)
            print(response.status_code)
            # download file
            with open('./art.zip', 'wb') as file:
                file.write(response.content)

            # extract file
            with ZipFile('./art.zip') as myzip:
                with myzip.open('public/widgets/summary.json') as myfile:
                    bot_nickname = eval(myfile.read())["reportName"]
                    if bot_name == bot_nickname:
                        myzip.extractall()
                        break


if __name__ == '__main__':

    try:
        bot_name = os.environ['BOT_NAME']
    except:
        bot_name = "all_bots"

    past_report(bot_name)
















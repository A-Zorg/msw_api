from allure_behave.hooks import allure_report
import configparser
from datetime import datetime, timedelta
import re
import pandas as pd
import requests
from base.ssh_interaction import create_user_session
import paramiko
import requests
import time


config = configparser.ConfigParser()
config.read("cred/config.ini")
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






import imaplib
import email
from email.header import decode_header


# account credentials
username = "sashella92@gmail.com"
password = "357951123Qwe!"
# create an IMAP4 class with SSL
with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    N = 1
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                            print(body)
                        except:
                            pass


    # close the connection and logout
    imap.close()
    imap.logout()




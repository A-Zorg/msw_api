from allure_behave.hooks import allure_report
import configparser
from datetime import datetime, timedelta
import re
import pandas as pd
import requests
from base.ssh_interaction import create_user_session
import random
import requests
config = configparser.ConfigParser()
config.read("cred/config.ini")
#
#
# sess = create_user_session(**config['fin_user'])
#
#
# url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
# bills = sess.get(url)
# text = bills.text
# template_list = ['Company Daily Ne',
#                      'Company ServComp',
#                      'Compaony Office Fees',
#                      'Company Net Income',
#                      'Company Social Fund'
#                      ]
#
# print([i in text for i in template_list])
# print(any([i in text for i in template_list]))
# sess.close()
a= {'asd':'ASD','fgh':'FGH'}

zero_date=datetime.now()
back_date = datetime(zero_date.year, zero_date.month, 1, 21, 59, 59, 999999)
reconciliation_date = back_date-timedelta(1)


#
# headers ={
#     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#
# }
# bills = sess.get(url, headers = headers)
#
# asd = re.findall('name="csrfmiddlewaretoken" value="(.+)">',bills.text)[0]
#
# date_x = datetime.today() - timedelta(5)
# print(date_x)
# a= requests.get('asdasd')

# recon_dict = {
#         'csrfmiddlewaretoken': asd,
#         'entry.date_to_execute': date_x,
#         'entry.description': 'asdasdasd',
#         'transaction_out.user_bill': '',
#         'transaction_out.company_bill': '95',
#         'transaction_in.user_bill': '',
#         'transaction_in.company_bill': '97',
#         'transaction_common.amount_usd': '13',
#         'transaction_common.description':'asdasd',
# }
# uo = sess.post(url, data= recon_dict, headers={"Referer": url})
# print(uo.status_code)
# print(uo.text)
#



from allure_behave.hooks import allure_report
import configparser
from datetime import datetime, timedelta
import re
import pandas as pd
import requests
from base.ssh_interaction import create_user_session
import random
# config = configparser.ConfigParser()
# config.read("cred/config.ini")
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
def random_filter_generator(item_list, patern):
    copy_list = item_list[:]
    qty = random.randint(0,len(copy_list))
    new_list=[]
    for i in range(qty):
        new_list.append(random.choice(copy_list))
        copy_list.remove(new_list[-1])
    url_parts = [f'{patern}[]={i}&' for i in new_list]
    return ''.join(url_parts), new_list
# ?user[]=141&user[]=77&account[]=2&account[]=3&date_from=2020-11-01T00:00:00&date_to=2020-12-31T00:00:00
dic = eval(r"{90000: [{'Current Net balance': 1171.0, 'id': 25420}, {'Cash hub': 21.0, 'id': 25419}, {'Account': 1, 'id': 25418}, {'Withdrawal': 162, 'id': 25417}, {'SmartPoints': 897, 'id': 25416}, {'Investments': 229, 'id': 25415}], 90001: [{'Current Net balance':-1093.0, 'id': 25426}, {'Cash hub': -226.0, 'id': 25425}, {'Account': 955, 'id': 25424}, {'Withdrawal': 220, 'id': 25423}, {'SmartPoints': -93, 'id': 25422}, {'Investments': 9, 'id': 25421}], 90002: [{'Current Net balance': -92.0, 'id': 25432}, {'Cash hub': 317.0, 'id': 25431}, {'Account': 15, 'id': 25430}, {'Withdrawal': 580, 'id': 25429}, {'SmartPoints': 1019, 'id': 25428}, {'Investments': 1028, 'id': 25427}], 0: [{'Company ServComp': 10969, 'id': 107}, {'Company Office Fees': 10835.0, 'id': 108}, {'Company Net Income': 10340.0, 'id': 109}, {'Company Social Fund': 10132, 'id': 110}, {'Company Daily Net': 10000, 'id': 111}]}")
user_list = [i for i in dic.keys()][:-1]

asd = [1,2,3,4,5,6,7,8,9]

print(random_filter_generator(user_list, 'user'))

print(asd)

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
#
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



from behave import *
from base.main_functions_class import MainFunc
import random


def random_filter_generator(item_list, patern):
    copy_list = item_list[:]
    qty = random.randint(0,len(copy_list))
    new_list=[]
    for i in range(qty):
        new_list.append(random.choice(copy_list))
        copy_list.remove(new_list[-1])
    url_parts = [f'{patern}[]={i}&' for i in new_list]
    return ''.join(url_parts), new_list


@step("get {subject} bills")
def step_impl(context, subject):
    if subject == 'company':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
    elif subject == 'user':
        url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/user/types/'

    worker = MainFunc(context.session, url)
    subject_dict = worker.json_list
    context.bill_list = [part['id'] for part in subject_dict]
    with open('C:\\Users\\wsu\\Desktop\\api.txt', 'a') as file:
        file.write(str(context.bill_list)+'\n')


@step("create url for journal entries")
def step_impl(context):
    user_list = [i for i in context.bills.keys()][:-1]

    url_users, users = random_filter_generator(user_list, 'user')
    url_accounts, accounts = random_filter_generator(context.bill_list, 'account')

    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entries/?'\
          +url_users\
          +url_accounts
    with open('C:\\Users\\wsu\\Desktop\\api.txt', 'a') as file:
        file.write(str(url)+'\n')


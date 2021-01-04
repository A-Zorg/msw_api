from behave import *
from base.main_functions_class import GetRequest


@step("check not authenticated person for api {url}")
def step_impl(context, url):
    session = context.stranger
    template = '{"detail":"Authentication credentials were not provided.","status_code":403}'

    request = session.get(f'https://mytest-server.sg.com.ua:9999/api{url}')
    assert template == request.text

@step("check {user} permissions for AS: {url} and {success}")
def step_impl(context,user, url, success):
    if user == 'fin':
        session = context.fin_user
    else:
        session = context.super_user
    request = session.options(f'https://mytest-server.sg.com.ua:9999/api{url}')
    # with open('C:\\Users\\wsu\\Desktop\\api.txt', 'a') as file:
    #     file.write(str(request.text)+'\n')

    success_result = eval(success)
    assert request.ok==success_result

@step("check manager's permissions for AS {url}")
def step_impl(context, url):
    session = context.manager_user
    template = '{"detail":"You do not have permission to perform this action.","status_code":403}'

    request = session.get(f'https://mytest-server.sg.com.ua:9999/api{url}')
    assert template == request.text


@step("check company bills list")
def step_impl(context):
    session = context.fin_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/company/'
    worker = GetRequest(session, url)
    template_list = ['Company Daily Net',
                     'Company ServComp',
                     'Company Office Fees',
                     'Company Net Income',
                     'Company Social Fund'
                     ]

    assert worker.check_text(template_list)

@step("check user bills list")
def step_impl(context):
    session = context.fin_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/user/types/'
    worker = GetRequest(session, url)
    template_list = ['Current Net balance',
                     'Cash hub',
                     'SmartPoints',
                     'Investments',
                     'Account',
                     'Withdrawal'
                     ]

    assert worker.check_text(template_list)

@step("check users bills")
def step_impl(context):
    session = context.fin_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/bills/users/'
    worker = GetRequest(session, url)

    lis = []
    for key, value in context.bills.items():
        for part in value:
            index = value.index(part) + 1
            id = part['id']
            lis.append([key, index, id])

    assert worker.check_json(lis)
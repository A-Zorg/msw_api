from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
import pandas as pd
import psycopg2
import datetime
import requests
import random
import configparser

config = configparser.ConfigParser()
config.read("cred/config.ini")




@step("get all books and sort by author")
def step_impl(context):
    url = f'https://mytest-server.sg.com.ua:9999/api/index/books/?search_string=' \
          f'&sections_id=&include=themes&limit=500&offset=0&sort_by=popularity' \
          f'&sort_order=desc'
    session = context.manager_user
    response = GetRequest(session, url)
    lib = response.json_list
    authors = {}
    for book in lib:
        if authors.get(book['author']):
            authors[book['author']].append(book['title'])
        else:
            authors[book['author']] = [book['title']]
    context.authors = authors

@step("create url with random author")
def step_impl(context):
    author_list = list(context.authors.keys())
    context.author = random.choice(author_list)

    context.url = f'https://mytest-server.sg.com.ua:9999/api/index/books/?search_string={context.author}' \
          f'&sections_id=&include=themes&limit=100&offset=0&sort_by=popularity' \
          f'&sort_order=desc'

@step("search of books")
def step_impl(context):
    url = context.url
    session = context.manager_user
    response = GetRequest(session, url)

    context.response = response.json_list

@step("check result of search")
def step_impl(context):
    exp_books = context.authors[context.author]
    act_books = [ book['title'] for book in context.response ]
    result = all([part in act_books for part in exp_books])

    assert result


"""______________________________________Holidays________________________________________"""

@step("get US holidays for this year")
def step_impl(context):
    countries = ['US', 'GB']
    holidays = {
        'New Year\'s Day': '',
        'Martin Luther King, Jr. Day': '',
        'Washington\'s Birthday': '',
        'Memorial Day': '',
        'Independence Day': '',
        'Labour Day': '',
        'Thanksgiving Day': '',
        'Christmas Day': '',
        'Good Friday': '',
                }
    for country in countries:
        url = f"https://public-holiday.p.rapidapi.com/2021/{country}"

        headers = {
            'x-rapidapi-key': config['holidays_api']['x-rapidapi-key'],
            'x-rapidapi-host': config['holidays_api']['x-rapidapi-host']
        }

        response = requests.get(
            url=url,
            headers= headers
        )
        for i in response.json():
            if holidays.get(i['name']) == '':
                holidays[i['name']] = datetime.date.fromisoformat(i['date'])
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a') as file:
    #     file.write(str(holidays) + '\n')
    holidays['Labor Day'] = holidays['Labour Day']
    context.exp_holidays = holidays

@step("compare holidays from endpoint")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/index/holidays/'
    session = context.manager_user
    response = session.get(url)

    formating = lambda part: '-'.join(part['date'].split('.')[::-1])

    act_holidays = {part['name'] : datetime.date.fromisoformat(formating(part)) for part in response.json()}
    result = [act_holidays[key] == context.exp_holidays[key] for key in act_holidays.keys()]

    assert all(result)

"""--------------------------------------------------CHECK SERV&COMP index_page-------------------------------------------------"""
@step("check /api/index/services_compensations/")
def step_impl(context):
    url = 'https://mytest-server.sg.com.ua:9999/api/index/services_compensations/'
    session = context.manager_user
    response = session.get(url)

    template = {
                "compensations": [
                    {
                        "name": "COMP",
                        "value": 200.0
                    }
                ],
                "services": [
                    {
                        "name": "SERV",
                        "value": -100.0
                    }
                ]
            }

    assert eval(response.text)==template

"""------------------------------CHECK /index/users/----------------------------------"""


@step("get users data from db")
def step_impl(context):
    with psycopg2.connect(**config['pg_db']) as con:
        cur = con.cursor()

        cur.execute("SELECT  g.id, g.name, array_agg(p.permission_id) "
                    "FROM public.auth_group as g "
                    "LEFT JOIN public.auth_group_permissions as p ON p.group_id = g.id "
                    "GROUP BY g.id"
                    )
        rows = cur.fetchall()
        groups={}
        for row in rows:
            groups[row[0]] = {
                "id": row[0],
                "name": row[1],
                "permissions": [] if row[2][0]==None else row[2]
            }
            groups[row[0]]['permissions'].sort()
        cur.execute("SELECT u.id, u.hr_id, u.first_name, u.last_name, u.patronymic, array_agg(g.id)"
                    "FROM public.index_customuser as u "
                    "LEFT JOIN public.index_customuser_groups as i ON i.customuser_id = u.id "
                    "LEFT JOIN public.auth_group as g ON i.group_id = g.id "
                    "WHERE u.hr_id > 0"
                    "GROUP BY u.id")
        rows = cur.fetchall()
        users=[]
        for row in rows:
            row[5].sort()
            users.append({
                "id": row[0],
                "hr_id": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "patronymic": row[4],
                "groups": [] if row[5][0]==None else [groups[i] for i in row[5]]
            })
        context.result = sorted(users, key=lambda i: i['id'])

@step("compare data from endpoint and db")
def step_impl(context):
    session = context.fin_user
    url = 'https://mytest-server.sg.com.ua:9999/api/index/users/'
    response = session.get(url)

    result = sorted(response.json(), key=lambda i: i['id'])
    [group['permissions'].sort()  for user in result for group in user['groups']]
    for user in result:
        user['groups'] = sorted(user['groups'], key=lambda i: i['id'])

    assert result == context.result


"""----------------------------------book category------------------------------------------"""
@step("get books categories from endpoint")
def step_impl(context):
    session = context.manager_user
    url = 'https://mytest-server.sg.com.ua:9999/api/index/books/categories/'
    response = session.get(url)
    context.act_categories = response.json()

    assert response.ok


@step("compare books_categories from endpoint and template")
def step_impl(context):
    with open('base/data_set/book_categories.txt', 'r',encoding='utf-8') as file:
        exp_categories = eval(file.read())

        assert exp_categories == context.act_categories

"""----------------------------------------------------------------"""













@step("probe {number}")
def step_impl(context, number):
    session = context.super_user
    url = 'https://mytest-server.sg.com.ua:9999/api/accounting_system/entry/'
    token = get_token(session,url)


    request_dict= {
                       'transaction_out.user_bill': '31482',
                       'transaction_out.company_bill': '',
                       'entry.date_to_execute': datetime.datetime.now(),
                       'entry.description': '',
                       'transaction_common.amount_usd': number,
                       'transaction_common.description': '',
                       'csrfmiddlewaretoken': token,
    }



    response = session.post(
                url,
                data=request_dict,
                headers={"Referer": url}
    )
    # with open('C:\\Users\\wsu\\Desktop\\xxx.txt', 'a', encoding='utf-8') as file:
    #     file.write(str(response.text) + '\n')







#
#
#
# SELECT u.id, u.hr_id, u.first_name, u.last_name, u.patronymic, g.id, g.name, p.permission_id
# FROM public.index_customuser as u
# LEFT JOIN public.index_customuser_groups as i ON i.customuser_id = u.id
# LEFT JOIN public.auth_group as g ON i.group_id = g.id
# LEFT JOIN public.auth_group_permissions as p ON p.group_id = g.id
#






















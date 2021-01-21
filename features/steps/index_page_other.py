from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
import pandas as pd
import psycopg2
import io
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
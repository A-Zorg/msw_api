from behave import *
from behave.api.async_step import async_run_until_complete
from base.main_functions import GetRequest, get_token, find_button
from behave.api.async_step import async_run_until_complete
import pandas as pd
import psycopg2
import io
import requests
from base64 import b64decode



""""----------------------------------------CHECK CONTEST IMAGES-----------------------------------------"""
@step("get endpoint image: {type_image}")
def step_impl(context, type_image):
    url = context.custom_config["host"] + f'api/media/contest/{type_image}/image'
    session = context.super_user
    response = GetRequest(session, url)

    image = response.json_list['image']
    head, body= image.split(',', 1)

    context.endpoint_image = io.BytesIO(b64decode(body))

@step("get endpoint image file")
def step_impl(context):
    data = context.endpoint_image
    data.name = '/endpoint_image.jpg'
    context.endpoint_image_file = io.BufferedReader(data)

@step("get new image")
def step_impl(context):
    context.new_image_file = open('base/data_set/clown.jpg', 'rb')
    context.new_image = context.new_image_file.read()
    context.new_image_file.seek(0)

@step("compare uploaded image with resulting image from endpoint")
def step_impl(context):
    assert context.new_image == context.endpoint_image.getvalue()

@step("upload {gen_image} through endpoint: {type_image}")
def step_impl(context, gen_image, type_image):
    url = context.custom_config["host"] + f'api/login/'
    response = requests.options(url)

    headers = {
        'X-CSRFToken': response.cookies['csrftoken']
    }

    data = {
        'username': context.custom_config["super_user"]["username"],
        'password': context.custom_config["super_user"]["password"],
        'name_key': type_image
    }
    if gen_image == 'new image':
        image = context.new_image_file
    elif gen_image == 'original image':
        image = context.endpoint_image_file
    files = {
        'image': image
    }
    response = requests.post(
        context.custom_config["host"] + f'api/media/contest/image_upload',
        headers=headers,
        data=data,
        files=files
    )
    assert response.ok


@step('upload {gen_image} through Riskbot: {type_image}')
@async_run_until_complete
async def send_fees_to_riskbot(context, gen_image, type_image):
    async with context.tele_user.conversation(context.custom_config["risk_bot"]) as conv:

        await conv.send_message('/start')
        message = await conv.get_response()
        button = find_button([message], 'Админ')
        await button.click()

        if type_image == 'top30':
            button_name = 'Топ-30'
        elif type_image == 'smartheat':
            button_name = 'SmartHeat'
        message = await conv.get_response()
        button = find_button([message], button_name)
        await button.click()
        await conv.get_response()

        if gen_image == 'new image':
            file = context.new_image_file
        elif gen_image == 'original image':
            file = context.endpoint_image_file
        await conv.send_file(file=file, force_document=True)
        message = await conv.get_response()
        assert 'успешно загружен, в том числе и на MySmartWeb' in message.text

@step("check contests endpoint: {cont_type}")
def step_impl(context, cont_type):
    url = context.custom_config["host"] + 'api/index/contests/'
    session = context.manager_user
    response = GetRequest(session, url)
    contests = response.json_list
    result = [contest for contest in contests if contest['name_key'] == cont_type and contest['button_thumb'].endswith('.png') and contest['image'].endswith('.jpg')]

    assert result
"""-----------------------------------CHECK CONTEST ICONS--------------------------------------"""

@step("get endpoint icon: {type_icon}")
def step_impl(context, type_icon):
    url = context.custom_config["host"] + f'api/media/contest/{type_icon}/button'
    session = context.super_user
    context.response = session.get(url)


@step("compare actual icon with expected icon: {type_icon}")
def step_impl(context, type_icon):
    with open(f'base/data_set/{type_icon}.png','rb') as file:
        exp_icon = file.read()
        act_icon = context.response.content
        assert exp_icon == act_icon

"""------------------------------------------CHECK NEWS------------------------------------------"""

@step("initiate news data")
def step_impl(context):
    context.image = open('base/data_set/clown.jpg','rb')
    context.title = 'super news'
    context.text_news = 'A ab aspernatur at, aut cumque dicta dolore doloribus dolorum ea, error est et excepturi\n fugiat fugit harum inventore iste laudantium, minima minus molestias nesciunt perspiciatis \nquasi quis repudiandae saepe similique sit! '

@step("create news")
def step_impl(context):
    url = context.custom_config["host"] + 'admin/index/news/add/'
    session = context.super_user
    token = get_token(session, url)

    headers = {
        "Referer" : url,
        "X-CSRFToken": token,
    }

    data = {
        'title': context.title,
        'text': context.text_news,
        '_save': 'Save',

    }

    files = {
        'image': context.image
    }
    response = session.post(
        url,
        headers=headers,
        data=data,
        files=files
    )

    assert response.ok

@step("get test_news id")
def step_impl(context):
    url = context.custom_config["host"] + 'api/index/news/'
    session = context.super_user
    response = GetRequest(session, url)
    items = response.json_list['items']
    test_news = ''

    for item in items:
        if item['title'] == context.title:
            test_news = item
    context.id = test_news['id']

    assert test_news['likes'] == 0 and test_news['views'] == 0


@step("perform {proc} process")
def step_impl(context, proc):
    url = context.custom_config["host"] + f'api/index/news/{context.id}/{proc}/'
    session = context.manager_user
    token = get_token(session, url, 'X-CSRFToken')

    headers = {
        "Referer": url,
        "X-CSRFToken": token,
    }
    response = session.post(
        url,
        headers=headers,
    )
    assert response.ok

@step("compare image of news with template image")
def step_impl(context):
    url = context.custom_config["host"] + f'api/media/news/{context.id}'
    session = context.manager_user
    response = session.get(url)
    context.image.seek(0)

    assert context.image.read() == response.content

@step("check all data of news")
def step_impl(context):
    url = context.custom_config["host"] + 'api/index/news/'
    session = context.super_user
    response = GetRequest(session, url)
    items = response.json_list['items']
    test_news=''

    for item in items:
        if item['id'] == context.id:
            test_news = item

    assert test_news['likes'] == 0 and test_news['views'] == 1 and test_news['title'] == context.title

@step("delete created news")
def step_impl(context):
    with psycopg2.connect(**context.custom_config['pg_db']) as con:
        cur = con.cursor()

        cur.execute(f"DELETE FROM index_postview WHERE post_id = {context.id};"
                    f"DELETE FROM index_news WHERE id = {context.id};")
        con.commit()





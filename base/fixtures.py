from behave import fixture
import configparser
import requests
from telethon import TelegramClient
from base.adminka import create_user_session

config = configparser.ConfigParser()
config.read("cred/config.ini")

session_dict = {
        'super_session': '',
        'fin_session': '',
        'manager_session': '',
        'stranger_session': '',
        'sb_user': '',
}
@fixture()
def session(context):
    """creating sessions"""
    session_dict['super_session'] = create_user_session(
        context.custom_config['host'],
        **context.custom_config['super_user']
    )
    # session_dict['fin_session'] = create_user_session(
    #     context.custom_config['host'],
    #     **context.custom_config['fin_user']
    # )
    session_dict['manager_session'] = create_user_session(
        context.custom_config['host'],
        **context.custom_config['manager_user']
    )
    session_dict['stranger_session'] = requests.Session()

    session_dict['sb_user'] = requests.Session()
    session_dict['sb_user'].post(
        url='https://hrtest-server.sg.com.ua/api/user/login',
        data = {
            "login": context.custom_config['sb_user']['login'],
            "password": context.custom_config['sb_user']['password'],
        }
    )

    context.super_user = session_dict['super_session']
    # context.fin_user = session_dict['fin_session']
    context.manager_user = session_dict['manager_session']
    context.stranger = session_dict['stranger_session']
    # context.sb = session_dict['sb_user']

    context.tele_user = TelegramClient(
        './cred/sess',
        context.custom_config['telegram_user']['api_id'],
        context.custom_config['telegram_user']['api_hash']
    ).start()

    yield

    # close the sessions
    context.tele_user.disconnect()
    for value in session_dict.values():
        value.close()






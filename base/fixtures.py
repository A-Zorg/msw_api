from behave import fixture
import configparser
import requests
from base.ssh_interaction import create_user_session
from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("cred/config.ini")

session_dict = {
        'super_session' : '',
        'fin_session' : '',
        'manager_session' : '',
        'stranger_session' : '',
}
@fixture()
def session(context):
    session_dict['super_session'] = create_user_session(**config['super_user'])
    session_dict['fin_session'] = create_user_session(**config['fin_user'])
    session_dict['manager_session'] = create_user_session(**config['manager_user'])
    session_dict['stranger_session'] = requests.Session()

    context.super_user = session_dict['super_session']
    context.fin_user = session_dict['fin_session']
    context.manager_user = session_dict['manager_session']
    context.stranger = session_dict['stranger_session']
    context.tele_user = TelegramClient('sess',
                                       config['telegram_user']['api_id'],
                                       config['telegram_user']['api_hash']
                                       ).start()
    yield

    context.tele_user.disconnect()

    for value in session_dict.values():
        value.close()






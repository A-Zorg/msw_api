from behave import fixture
import configparser
import requests
from base.ssh_interaction import create_user_session
import time

config = configparser.ConfigParser()
config.read("cred/config.ini")

@fixture()
def session(context, user_tag):
    if user_tag == 'none_user' or user_tag == None:
        session = requests.Session()
        context.session = session
    else:
        session = create_user_session(**config[user_tag])
        context.session = session
    yield
    session.close()
    time.sleep(0)





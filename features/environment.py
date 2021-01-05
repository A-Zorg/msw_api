from behave import use_fixture
from base.fixtures import session
from base.ssh_interaction import cleaner, loader, start_reconciliation, stop_reconciliation
from base.data_set_creater import data_set_reconciliation, add_number_bills
from allure_behave.hooks import allure_report
import configparser
import copy

config = configparser.ConfigParser()
config.read("cred/config.ini")


# def before_feature(context, feature):
#     user_tag = feature.tags[0]
#     use_fixture(session, context, user_tag)

def before_all(context):
    # loader(**config['server'])
    use_fixture(session, context)
    # start_reconciliation(config['super_user'])
    # stop_reconciliation(config['super_user'])
    bills, entries = data_set_reconciliation()
    context.bills, context.entries, context.userdata = add_number_bills(context.fin_user, bills, entries)
    context.modified_bills = copy.deepcopy(context.bills)


def after_all(context):
    # cleaner(**config['server'])
    print(context.modified_bills==context.bills)






#
# """create allure reports"""
# allure_report("reports/")

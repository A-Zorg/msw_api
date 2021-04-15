import copy
import os
from behave import use_fixture
from base.google_sheet import update_gs
from allure_behave.hooks import allure_report
from base.fixtures import session
from base.adminka import finish_reconciliation_process
from base.main_functions import get_custom_config
from base.ssh_interaction import upload_files_server, runner
from base.data_set_creater import data_set_reconciliation, add_number_bills
from generator.total_generation import generate_data
from base.create_fees_riskbot import create_riskbot_fees, make_accounting_precondition

os.environ['TEST_HOST'] = 'test_9999'
def before_all(context):
    """create custom_config"""
    try:
        host = os.environ['TEST_HOST']
    except:
        host = 'test'
    get_custom_config(context, host)

    # """create data set"""
    # generate_data(5, context)
    #
    # """upload dataset to the server"""
    # upload_files_server(context)
    #
    # """upload dataset to msw"""
    # runner(context, "loader.py")

    # """upload data to SERV&COMP table"""
    # update_gs()
    #
    # """create file FEES to upload through riskbot"""
    # create_riskbot_fees()

    """create sessions of users"""
    use_fixture(session, context)

    # """make precondition steps to check ACCOUNTING"""
    # make_accounting_precondition(context)
    #
    # """perform reconciliation"""
    # finish_reconciliation_process(context)

    """generate vars with data"""
    bills, entries = data_set_reconciliation()
    context.bills, context.entries, context.userdata = add_number_bills(context, bills, entries)
    context.modified_bills = copy.deepcopy(context.bills)

def after_all(context):
    """delete all generated data"""
    runner(context, "cleaner.py")

# """create allure reports"""
# allure_report("allure-results/")

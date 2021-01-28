from behave import use_fixture
from base.fixtures import session
from base.ssh_interaction import cleaner, loader, start_reconciliation, stop_reconciliation, upload_server
from base.data_set_creater import data_set_reconciliation, add_number_bills
from allure_behave.hooks import allure_report
from generator.total_generation import generate_data
import configparser
from base.google_sheet import update_gs
from base.create_fees_riskbot import create_riskbot_fees, make_accounting_precondition
import copy

config = configparser.ConfigParser()
config.read("cred/config.ini")


def before_all(context):
    # """create data set"""
    # generate_data(10)
    #
    # """upload dataset to the server"""
    # upload_server(**config['server'])
    #
    # """upload dataset to msw"""
    # loader(**config['server'])
    #
    # """upload data to SERV&COMP table"""
    # update_gs()
    #
    # """create file FEES to upload through riskbot"""
    # create_riskbot_fees()

    """create sessions of users"""
    use_fixture(session, context)

    # """make precondition steps to check ACCOUNTING"""
    # make_accounting_precondition(config['manager_id']['hr_id'], context)

    # """perform reconciliation"""
    # start_reconciliation(context.super_user)
    # stop_reconciliation(context.super_user)
    #
    # """generate vars with data"""
    # bills, entries = data_set_reconciliation()
    # context.bills, context.entries, context.userdata = add_number_bills(context.fin_user, bills, entries)
    # context.modified_bills = copy.deepcopy(context.bills)


#
# def after_all(context):
#     """delete all generated data"""
#     cleaner(**config['server'])



"""create allure reports"""
allure_report("reports/")

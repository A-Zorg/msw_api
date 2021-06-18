Feature: import from propreports

#
#  Scenario: prepare conditions for testing import from propreports
#    Given clear db table: reconciliation_reconciliationuserpropaccount
#     And clear db table: reconciliation_userpropaccount
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And run the task: download_from_propreports_monthly
#     And wait for task is finished: month_propreports_files_parsing
#    When upload to the server some file and run it: month_propreports
#     And modification of msw db to provoke running of bills_corrections by month_propreports_modificator - without mod - None
#    Then get amount of users (90000, 90001) Current Net balance
#     And compare sum of Month Adj Net of accounts with Current Net balance sum of users

#
#    Scenario:gsdfgsdfgsdfg
#    Given clear db table: reconciliation_reconciliationuserpropaccount
#     And clear db table: reconciliation_userpropaccount
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And run the task: download_from_propreports_monthly
#     And wait for task is finished: month_propreports_files_parsing
#    When asdupload to the server some file and run it: month_propreports
# Scenario:haos
#    Given protoffffffffffffffffffffffffffffffffffffffffffffffffffftype
#  Given hnia

#  Scenario Outline: checking different types of corrections after month import from propreports
#    Given check that 2 active accounts exist
#     And modification of msw db to provoke running of bills_corrections by month_propreports_modificator - <phrase> - <modifier>
#     And get amount of users (90000, 90001) Current Net balance
#    When run the task: download_from_propreports_monthly
#     And wait for task is finished: month_propreports_files_parsing
#     And run the task: entries_for_prop_month_correction
#    And pause - 20 sec(s)
#     And get amounts(<qty>) from the monthpropreportstransactios table and check users Current Net balance
#     And compare sum of Month Adj Net of accounts with Current Net balance sum of users
#    Examples:
#        |  phrase                                       |   modifier                                  | qty |
#        |  len(adj_net_list)-adj_net_list.count(0)==0   |   ["zero->create", "zero->create"]          |  2  |
#        |  0<adj_net_list.count(0)<len(adj_net_list)    |   ["zero->create"]                          |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)==0   |   ["zero->create"]                          |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->change", "non zero->change"]  |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->change"]                      |  1  |
#        |  0<adj_net_list.count(0)<len(adj_net_list)    |   ["non zero->change"]                      |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->delete", "non zero->delete"]  |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->delete"]                      |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->delete"]                      |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   [ "non zero->delete", "non zero->change"] |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->delete", "zero->create"]      |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->change", "zero->create"]      |  2  |


#  Scenario Outline: checking different types of corrections after month import from propreports
#    Given check that 1 active accounts exist
#     And modification of msw db to provoke running of bills_corrections by month_propreports_modificator - <phrase> - <modifier>
#     And get amount of users (90000, 90001) Current Net balance
#    When run the task: import_from_propreports_monthly
#     And wait for task is finished: entries_for_prop_month_correction
#     And get amounts(<qty>) from the monthpropreportstransactios table and check users Current Net balance
#     And compare sum of Month Adj Net of accounts with Current Net balance sum of users
#    Examples:
#        |  phrase                                       |   modifier             | qty |
#        |  len(adj_net_list)-adj_net_list.count(0)==0   |   ["zero->create"]     |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->delete"] |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->change"] |  1  |


  Scenario: prepare conditions for testing import from propreports
    Given clear db table: reconciliation_reconciliationuserpropaccount
     And clear db table: reconciliation_userpropaccount
     And run the task: import_HR_module
     And wait for task is finished: import_HR_module
     And run the task: download_from_propreports_monthly
     And wait for task is finished: month_propreports_files_parsing
     And upload to the server some file and run it: month_propreports
     And clear db table: accounting_system_companypropaccountdata
     And clear db table: accounting_system_companypropaccount
    When migrate user accounts to company
     And clear db table: reconciliation_reconciliationuserpropaccount
     And clear db table: reconciliation_userpropaccount
     And run the task: download_from_propreports_monthly
     And wait for task is finished: month_propreports_files_parsing
    Given modification of msw db to provoke running of bills_corrections by company_month_modificator2 - without mod - None
     And compare month_adj_net with sum(daily_adj_net) of company_prop_account

  Scenario Outline: checking different types of corrections after month import from propreports
    Given check that 2 active accounts of company exist
     And modification of msw db to provoke running of bills_corrections by company_month_modificator2 - <phrase> - <modifier>
    When run the task: download_from_propreports_monthly
     And wait for task is finished: month_propreports_files_parsing
     And run the task: entries_for_prop_month_correction
    And pause - 30 sec(s)
     Then amounts from the monthpropreportstransactios table should be <qty>
     And compare month_adj_net with sum(daily_adj_net) of company_prop_account
     And check companybill OPERATIONAL
    Examples:
        |  phrase                                       |   modifier                                  | qty |
       |  len(adj_net_list)-adj_net_list.count(0)==0   |   ["zero->create", "zero->create"]          |  2  |
#       |  0<adj_net_list.count(0)<len(adj_net_list)    |   ["zero->create"]                          |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)==0   |   ["zero->create"]                          |  1  |
        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->change", "non zero->change"]  |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->change"]                      |  1  |
#        |  0<adj_net_list.count(0)<len(adj_net_list)    |   ["non zero->change"]                      |  1  |
        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->delete", "non zero->delete"]  |  2  |
#        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->delete"]                      |  1  |
#        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   ["non zero->delete"]                      |  1  |
        |  len(adj_net_list)-adj_net_list.count(0)>=2   |   [ "non zero->delete", "non zero->change"] |  2  |
        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->delete", "zero->create"]      |  2  |
        |  len(adj_net_list)-adj_net_list.count(0)==1   |   ["non zero->change", "zero->create"]      |  2  |





#
















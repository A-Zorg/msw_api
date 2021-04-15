Feature: import from smartbase


#  Scenario: task import_hr_module
#    Given clear all data related to user: sb_user
#     And get data from SM about user: sb_user
#    When run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And get data from DB about user: sb_user
#    Then compare data from DB and SB
#     And should be created 6 different bills of user: sb_user
#


#  Scenario Outline: account regex(MSW-410)
#    Given add trading account with name <acc_name> to user: sb_user
#     And clear db table: reconciliation_reconciliationuserpropaccount
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And check <action_1> account <acc_name>-<acc_regex> in reconciliationuserpropaccount table
#     And delete trading account with name <acc_name> to user: sb_user
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And check absence account <acc_name>-<acc_regex> in reconciliationuserpropaccount table
#    Examples:
#        | acc_name     | acc_regex            | action_1 |
#        | SMRT056 asd  | ^SMRT[0-9]{3}$       | presence |
#        | STSTRADER023 | ^STSTRADER[0-9]{3}$  | presence |
#        | SMRT003NT 12 | ^SMRT[0-9]{3}N(T)?$  | presence |
#        | STS343       | ^STS[0-9]{3}$        | presence |
#        | STS343N a4d  | ^STS[0-9]{3}N(T)?$   | presence |
#        | EQS023 asd   | ^EQS[0-9]{3}$        | presence |
#        | EQS023N asd  | ^EQS[0-9]{3}N(T)?$   | presence |
#        | 34504123     | ^34504[0-9]{3}$      | presence |
#        | 34546789 af  | ^3454[0-9]{4}$       | presence |
#        | EQS023Nasd   | ^EQS[0-9]{3}$        | absence  |
#        | wqeEQS023N   | ^EQS[0-9]{3}$        | absence  |
#        | 12345678     | ^3454[0-9]{4}$       | absence  |

#
#  Scenario: check repairing userdata by task import_hr_module(MSW-460)
#    Given clear all data related to user: sb_user
#     And get data from SM about user: sb_user
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#    When change personal data of user: sb_user
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#     And get data from DB about user: sb_user
#    Then compare data from DB and SB
#


#  Scenario: MSW-552
#    Given get data from SM about user: sb_user
#     And add trading account with name SMRT056 to user: sb_user
#     And add trading account with name SMRT056 to user: sb_user
#    When clear db table: reconciliation_reconciliationuserpropaccount
#     And run the task: import_HR_module
#     And wait for task is finished: import_HR_module
#    Then check that account(s) == 1 in reconciliationuserpropaccount: sb_user
#     And get data from SM about user: sb_user
#
#
#
#














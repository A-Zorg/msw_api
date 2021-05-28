@super_user @manager_user
Feature:  reconciliation update
#
#  Scenario: check task "transfer_account_to_reconciliation" feature(MSW-537)
#      Given fields of userdata of user 90000 should be not none
#       And run the task: delete_reconciliation_data
#       And pause - 2 sec(s)
#       Given fields of userdata of user 90000 should be none
#       And get bills: 'Account', 'Current Net balance' of user 90000
#       And create the set of history_user_bill of user 90000
#      When run the task: transfer_bills_to_reconciliation
#       And wait for task is finished: transfer_bills_to_reconciliation
#      Then compare actual with expected fields: account and prev_month_net of user 90000
#
#  Scenario: check update_user_totals_before_reconciliation (MSW-568)
#    Given run the task: delete_reconciliation_data
#     And pause - 2 sec(s)
#     And run the task: create_bonus_fees
#     And wait for task is finished: update_user_totals_before_reconciliation
#    When [services]get total_service of user 90000
#     And [services]get total_compensation of user 90000
#     And [services]get total_fee of user 90000
#     And [account]get total_Takion of user 90000
#     And [account]get total_Broker of user 90000
#     And get user_totals from UserData of user 90000
#    Then compare actual_total with expected_total


  Scenario Outline: check "Entries created" feature(MSW-398)
      Given get bills id of user 90000
       And get all transactions of user 90000 before reconciliation
       And field -entries created- == <entries created>
       And field -date_reconciliation- == <reconciliation date>
      When perform RECONCILIATION
       And get all transactions of user 90000 after reconciliation
      Then compare transactions qty before and after RECONCILIATION <equality>
       And field -entries created- should be equal to <result>

    Examples:
      | entries created  | reconciliation date | equality   | result  |
      | true             | today midday        |  true      | True    |
      | false            | yesterday           |  true      | False   |
      | false            | tomorrow            |  true      | False   |
      | false            | today late          |  false     | True    |
      | false            | today early         |  false     | True    |

  Scenario: check "Entries created" feature(MSW-398)
      Given check userdata fields of user 90000 before -delete_reconciliation_data-
      When run the task: delete_reconciliation_data
      Then check userdata fields of user 90000 after -delete_reconciliation_data-


  Scenario Outline: check autoreconciliation (MSW-540)
      Given run the task: delete_reconciliation_data
       And change field -prev_month_net- in UserData table of user with hr_id 90000 to <amount>
       And change field -services_total- in UserData table of user with hr_id 90000 to -200
       And change field -qty_of_reconciliations- in UserData table of user with hr_id 90000 to <qty_rec>
       And field -entries created- == <entries created>
       And field -date_reconciliation- == <reconciliation date>
       And get bills id of user 90000
       And get all transactions of user 90000 before reconciliation
      When perform RECONCILIATION
       And get all transactions of user 90000 after reconciliation
      Then compare transactions qty before and after RECONCILIATION <equality>
    Examples:
     | amount     | entries created  | reconciliation date | equality   | qty_rec  |
     | -150000    | false            | null                |  true      | 0        |
     | -150000    | false            | null                |  true      | 1        |
     | -150000    | false            | today midday        |  false     | 0        |
     | -150000    | true             | null                |  true      | 0        |
     | 150000     | false            | null                |  true      | 0        |
     | -150000    | true             | null                |  true      | 1        |


#  Scenario Outline: Bonuses(MSW-510)
#      Given clear db table: reconciliation_bonus
#       And clean DB table: reconciliation_reconciliationuserpropaccount where user_id 90000
#       And clean DB table: reconciliation_service where user_id 90000
#       And get random account_type: -all-
#       And create or update user -90000- propaccount -bonus_acc- with <acc_value_1>
#       And create or update BONUS with <percentage>
#      When run the task: create_bonus_fees
#       And wait for task is finished: update_user_totals_before_reconciliation
#       And BONUS fee of user 90000 should be equal to -<result_1>-
#      Then create or update user -90000- propaccount -bonus_acc- with <acc_value_2>
#       And run the task: create_bonus_fees
#       And wait for task is finished: update_user_totals_before_reconciliation
#      And BONUS fee of user 90000 should be equal to -<result_2>-
#
#    Examples:
#     | acc_value_1 | percentage | result_1 | acc_value_2 | result_2 |
#     | 505.56      | 0.2        | 101.112  |  300        | 60       |
#     | 305.136     | 0.23       | 70.1813  |  0          | none     |
#     | 135.86      | 0.63       | 85.5918  |  -90        | none     |
#     | 0           | 0.2        | none     |  1245       | 249      |
#     | 0           | 0.4        | none     |  -300       | none     |
#     | -100        | 0.1        | none     |  3345.25    | 334.525  |
#     | -35         | 0.13       | none     |  0          | none     |
#
#  Scenario Outline: Rounding(MSW-549)
#    Given clean DB table: reconciliation_reconciliationuserpropaccount where user_id 90000
#     And clean DB table: reconciliation_service where user_id 90000
#     And change field -prev_month_net- in UserData table of user with hr_id 90000 to 1000
#     And get random account_type: -takion-
#     And create or update user -90000- propaccount -takion_1- with <first_number>
#     And create or update user -90000- propaccount -takion_2- with <second_number>
#     And get random account_type: -sterling-
#     And create or update user -90000- propaccount -sterling_1- with <first_number>
#     And create or update user -90000- propaccount -sterling_2- with <second_number>
#     And create or update user -90000- -service- with name -serv_1-, value -<first_number>-
#     And create or update user -90000- -service- with name -serv_2-, value -<second_number>-
#     And create or update user -90000- -compensation- with name -comp_1-, value -<first_number>-
#     And create or update user -90000- -compensation- with name -comp_2-, value -<second_number>-
#     And create or update user -90000- -fee- with name -fee_1-, value -<first_number>-
#     And create or update user -90000- -fee- with name -fee_2-, value -<second_number>-
#    When run the task: update_user_totals_before_reconciliation
#     And wait for task is finished: update_user_totals_before_reconciliation
#    Then check total_takion in UserData table: <first_number> and <second_number>
#     And check total_sterling in UserData table: <first_number> and <second_number>
#     And check services_total in UserData table: <first_number> and <second_number>
#     And check compensations_total in UserData table: <first_number> and <second_number>
#     And check office_fees in UserData table: <first_number> and <second_number>
#     And check total_net_month in UserData table: <total_net_month> and 0
#
#    Examples:
#     | first_number | second_number | total_net_month |
#     | 0.25         | 0.25          | 1004            |
#     | 123.4        | 904.0999      | 5108            |
#     | 8.0001       | 3             | 1044            |
#     | 23.75        | 99.2499       | 1492            |
#     | -0.3         | -0.2          | 996             |
#     | -6.25        | -99.2499      | 580             |
#     | -1.8         | -1000.1999    | -3008           |
#     | -0.7         | -76.6         | 692             |
#     | 0.6          | -0.2          | 1000            |
#
#
#
#  Scenario: perform reconciliation with custom_podushka(MSW-570)
#      Given change field -custom_podushka- in UserData table of user with hr_id 90000 to True
#       And check custom_podushka of user 90000 (should be True)
#      When run the task: clear_custom_podushka
#       And pause - 2 sec(s)
#      Then check custom_podushka of user 90000 (should be False)
#
#  Scenario: select date of reconciliation (MSW-568)
#      Given get expected [RC] tasks(qty:8)
#       And pick date of start: aftertomorrow
#      When make post request /reconciliation/date_of_reconciliation/
#       And get actual [RC] tasks(qty:8)
#      Then compare expected and actual [RC] tasks

  Scenario: Reconciliation API updates(MSW-692)
      Given get 90000 user's accounts which belong to subdomain sts through api
       And get to these accounts propreports_id and group_id through api
      When get 90000 user's accounts which belong to subdomain sts through db
       And get to these accounts propreports_id and group_id through db
      Then compare data from db and api










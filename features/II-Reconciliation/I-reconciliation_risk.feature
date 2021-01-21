@super_user @manager_user
Feature:  check all user_data

  Scenario: check all user_data
      Given get all user_data
       And get user_data from dataset
      Then compare userdata lists


  Scenario Outline: set the date of reconciliation
      Given pick date of start: <date>
       And make posr request /reconciliation/date_of_reconciliation/
      Then check data of response: <exp_res>
    Examples: forward
        |  date       |exp_res                              |
        |  yesterday  |Specified day is less or equal       |
        |  today      |Specified day is less or equal       |
        |  next_month |Specified day is not from this month |
        |  tomorrow   |Tasks created                        |


    Scenario: check reports update
      Given check status of "reports update": false
       And activate upload from propreports
      When pause - 240 sec(s)
      Then check status of "reports update": true

    Scenario: check services and compensations update
      Given check status of "services and compensations update": false
       And activate upload from services and compensations googlesheet
      When pause - 10 sec(s)
      Then check status of "services and compensations update": true


    Scenario: check risk update
      Given check status of "risk update": false
       And activate upload through riskbot
      When pause - 20 sec(s)
      Then check status of "risk update": true

    Scenario: check hr import
      Given clear reconciliationuserpropaccount table
       And activate hr_import
      Then check reconciliationuserpropaccount table after hr import

  Scenario: check hr import
      Given download all_users_data.xlsx
       When parse downloaded all_users_data.xlsx to compare with data from /reconciliation/all_users_data/
      Then compare downloaded data with data from /reconciliation/all_users_data/


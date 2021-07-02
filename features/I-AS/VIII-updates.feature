@fin_user
Feature: AS updates

  Scenario: create entries for JE
    Given get user and company bill_id
     And create PROPREPORTS entries:-Nomura-, -EQS-, -Broker 5-, -1-, -123-
     And create PROPREPORTS entries:-Nomura-, -SMRT-, -Broker 5-, -0-, --45.34-
     And create PROPREPORTS entries:-default-, -STS-, -Broker 5-, -1-, -99.1234-
     And create PROPREPORTS entries:-default-, -EQS-, -Takion-, -0-, -0.9999-
     And create PROPREPORTS entries:-default-, -STS-, -Takion-, -1-, -122143-
     And create PROPREPORTS entries:-default-, -EQS-, -Broker 4-, -0-, --333.333-

  Scenario Outline: JE
    Given get user and company bill_id
     And fin_user get broker list
     And fin_user get clearing list
     And fin_user get company list
     And get user bills
     And create url with filters: <company>, <broker>, <clearing>, <side>
    When by FIN create journal entries report
    Then check actual result of JE report with expected: <result>

      Examples:
        |  company  | broker    | clearing | side | result      |
        |  all      | Broker 5  |   all    | all  | 176.7834    |
        |  all      | all       |   Nomura | all  | 77.66       |
        |  STS      | all       |   all    | all  | 122242.1234 |
        |  EQS      | Broker 5  |   Nomura | all  | 123         |
        |  STS      | Takion    |   default| all  | 122143      |
        |  EQS      | Broker 4  |   default| all  | -333.333    |
        |  STS      | Broker 4  |   default| all  | 0           |
        |  all      | all       |   all    | 1    | 122365.1234 |
        |  SMRT     | Broker 5  |   Nomura | 1    | 0           |
        |  SMRT     | Broker 5  |   Nomura | 0    | -45.34      |
        |  all      | Broker 5  |   all    | 1    | 222.1234    |

  Scenario Outline:  NET buyout(MSW-512)
    Given change field -custom_payout_rate- in UserData table of user with hr_id 90000 to <custom_payout>
     And get 90000 user bills: Current Net balance, <from_account> and company bill: Company Net Income
     And [NET buyout] get bills amount before request
    When post request to perform NET buyout: <amount>
     And pause - 5 sec(s)
     And [NET buyout] get bills amount after request
    Then check bills after NET buyout: <amount>, <custom_payout>
     And check transactions after NET buyout

      Examples:
        |  custom_payout  | from_account | amount       |
        |  0.6            | Account      | 400.5271     |
        |  0.7312         | Withdrawal   | 60000        |
        |  0.5            | Account      | 60000.9999   |
        |  0              | Withdrawal   | 60000        |
        |  0              | Account      | 60000.0001   |
        |  0              | Withdrawal   | 9999999.4999 |
        |  0              | Account      | 40000.5555   |

  Scenario Outline:  NET buyout(MSW-512) errors
    Given [NET buyout] create request boy template
     And [NET buyout] change field -<field>- to <value>
     And [NET buyout] field -transaction_out.user_bill- == <in_bill>
     And [NET buyout] field -transaction_in.user_bill- == <out_bill>
    When [NET buyout] post request
    Then check actual result with expected <result>

      Examples:
        |  field                         | value            | in_bill         | out_bill                  |  result                                                               |
        |  entry.description             | none             | 90000 Account   | 90000 Current Net balance |  This field is required                                               |
        |  entry.description             | NET buyout       | 90000 Cash hub  | 90000 Current Net balance |  UserBill should be in list ['Account', 'Withdrawal']                 |
        |  entry.description             | NET buyout       | 90001 Account   | 90000 Current Net balance |  Two different users in transactions: 90001, 90000                    |
        |  entry.description             | NET buyout       | 90000 Account   | 90001 Current Net balance |  Two different users in transactions: 90000, 90001                    |
        |  entry.description             | NET buyout       | 90000 Account   | 90000 Cash hub            |  UserBill should be in list ['Current Net balance']                   |
        |  transaction_common.amount_usd | 123123.123123123 | 90000 Account   | 90000 Current Net balance |  Ensure that there are no more than 4 decimal places                  |
        |  transaction_common.amount_usd | 23123123127.31232| 90000 Account   | 90000 Current Net balance |  Ensure that there are no more than 15 digits in total                |
        |  transaction_common.amount_usd | 999999999999     | 90000 Account   | 90000 Current Net balance |  Ensure that there are no more than 11 digits before the decimal point|
        |  transaction_common.amount_usd | 99999999999      | 90000 Account   | 90000 Current Net balance |  entry                                                                |




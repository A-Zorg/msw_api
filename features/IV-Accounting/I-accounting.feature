Feature: check ACCOUNTING

#  Scenario: upload file through Riskbot
#    Given upload manager's account data through Riskbot
#
#
#  Scenario Outline: check ACCOUNTING part of MSW api
#    Then get data from accounting:<type>
#     And in accounting compare s expected with actual <type>
#    Examples: forward
#        |  type          |
#        |  account_data  |
#        |  account_queue |
#
#  Scenario Outline: check xlsx file from ACCOUNTING part of MSW
#    Given download <type> xlsx
#    Then in accounting compare expected with actual <type> file
#        Examples: forward
#        |  type          |
#        |  account_data  |
#        |  account_queue |




    Scenario: Accounting MSW-651
        Given delete manager_user bills: account and withdrawal and UserMainData
         And create manager_user bills: account and withdrawal
         When create default ENTRIES with parameters
            | amount | user_bill | day | month      |
            |  -12   |  Account  |  15 | before last|
            |   9.5  |  Account  |  26 | before last|
            |  -152.1 |  Account  |  15 | last       |
            |   10   |  Account  |  26 | last       |
            |   12.55|  Account  |  1  | this       |
            |   1234 | Withdrawal|  26 | before last|
            |  -12   | Withdrawal|  15 | before last|
            |   9.99 | Withdrawal|  26 | last       |
            |  -11.49| Withdrawal|  15 | last       |
            |   5    | Withdrawal|  1  | this       |
          And create expected result for Account
          And create expected result for Withdrawal
        Then compare manager actual and expected Account results
         And compare manager actual and expected Withdrawal results
         And compare by risk actual and expected Account results
         And compare by risk actual and expected Withdrawal results


    Scenario Outline: check given transactions in Accounting(MSW-651)
      Given get transactions data from db - bill:<user_bill>, month:<month>
       And compare by risk and manager actual and expected <user_bill> results for <month> month
       Examples:
        |  user_bill   |  month       |
        |  Account     |  last        |
        |  Account     |  before last |
        |  Withdrawal  |  last        |
        |  Withdrawal  |  before last |

    Scenario: User dataset creation for reports and journal entries (MSW-651)
        Given delete manager_user bills: account and withdrawal and UserMainData
         And create manager_user bills: account and withdrawal
         When create default ENTRIES with parameters
            | amount | user_bill | day | month      |
            |  -12   |  Account  |  15 | before last|
            |   9.5  |  Account  |  26 | before last|
            |  -152.1|  Account  |  15 | last       |
            |   10   |  Account  |  26 | last       |
            |   12.55|  Account  |  1  | this       |
            |   1234 | Withdrawal|  26 | before last|
            |  -12   | Withdrawal|  15 | before last|
            |   9.99 | Withdrawal|  26 | last       |
            |  -11.49| Withdrawal|  15 | last       |
            |   5    | Withdrawal|  1  | this       |
          And create UserMainData for manager user
            | services | compensations | fees | prev_month | total_net | plus_minus | zp_cash | company_cash | social | withdrawal | month        |
            |  -100    |  200          |  -15 | 345        | 34        | 12         | 1000    | 500          | 9      | 45         | last         |
            |  -200    |  300          |  -25 | 25         | 800       | 34         | 300     | 200          | 10     | 90         | before last  |

    @autorepeat @20
    Scenario: User reports (MSW-651)
      Given create random MANAGER report url and get actual result
      When get expected MANAGER report result
      Then compare actual and expected result of MANAGER report

    @autorepeat @20
    Scenario: User journal entries (MSW-651)
      Given get actual MANAGER journal entries with random data
      When get expected MANAGER journal entries with random data
      Then compare actual and expected result of MANAGER journal entries
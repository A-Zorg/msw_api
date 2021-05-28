Feature: report

  Scenario Outline: checking filters of REPORTS
    Given get user bills for reports
     And get report_fields
     And formation of url for report: <filter> with non actual date
    When get expected report data: <filter>
    Then compare expected report and actual report
    Examples: filter
        |  filter   |
        |  user     |
        |  account  |
        |  field    |
  Scenario Outline: checking filters of REPORTS
    Given get user bills for reports
     And get report_fields
     And formation of url for report: <filter> with actual date
    When get expected report data: <filter>
    Then compare expected report and actual report
    Examples: filter
        |  filter   |
        |  user     |
        |  account  |
        |  field    |

  Scenario: checking filters of REPORTS
    Given get company bills for reports
     And formation of url for company report with actual date
    When get expected company report data
    Then compare expected report and actual report

  Scenario: checking filters of REPORTS
    Given get company bills for reports
     And formation of url for company report with non actual date
    When get expected company report data
    Then compare expected report and actual report

  Scenario Outline: boundary values of entry fields
    Given define template request form
     And get csrf token
     And change request: field - <field>, value - <value>
    When make post request
    Then check actual result with expected <result>
    Examples: forward
        | field                           | value             | result                                                                  |
        |  transaction_common.amount_usd  | sdasd             |  A valid number is required                                             |
        |  transaction_common.amount_usd  | 1,45              |  A valid number is required                                             |
        |  transaction_common.amount_usd  | 234               |  entry                                                                  |
        |  transaction_common.amount_usd  | 99999999999       |  entry                                                                  |
        |  transaction_common.amount_usd  | 999999999999      |  Ensure that there are no more than 11 digits before the decimal point. |
        |  transaction_common.amount_usd  | 99999999999.1111  |  entry                                                                  |
        |  transaction_common.amount_usd  | 99999999999.11111 |  Ensure that there are no more than 15 digits in total.                 |
        |  entry.date_to_execute          | 2020-12-12        |  Datetime has wrong format. Use one of these formats instead            |
        |  transaction_out.company_bill   | 110               |  Bill should be only one!                                               |
        |  transaction_out.user_bill      | del               |  entry                                                                  |
        |  entry.description              | null              |  description":["This field is required                                                                 |

  Scenario Outline: boundary values of mass transaction fields
    Given define template request form of mass transaction
     And change request: <command>
    When post request to create mass transaction
    Then check actual result with expected <result>


        Examples: forward
        | command                                                                                                                                                | result                                                                    |
        |  [['del', ["mass_transaction_in",0]]]                                                                                                                  |  entry                                                                    |
        |  [['del', ["mass_transaction_in",0]], ['change', ["mass_transaction_in",0,'asd']]]                                                                     |  A valid number is required                                               |
        |  [['del', ["mass_transaction_in",0]], ['change', ["mass_transaction_out",1,8]], ['del', ["mass_transaction_out",0]]]                                   |  Non null field user_bill in transaction                          |
        |  []                                                                                                                                                    |  Not possible to create multiple transactions on both sides in one entry  |
        |  [['del', ["mass_transaction_in",1]]]                                                                                                                  |  Sum of the transaction on both sides are not equal                       |
        |  [['del', ["mass_transaction_in",0]],  ['del', ["mass_transaction_out",0]], ['del', ["mass_transaction_in",0]], ['del', ["mass_transaction_out",0]]]   |  Need to specify both sides of the entry                                  |
        |  [['del', ["mass_transaction_in",0]], ['change', ["mass_transaction_out",1,4.12345]], ['change', ["mass_transaction_out",1,3.87655]]]                  |  Ensure that there are no more than 4 decimal places                      |

Scenario Outline: cancel applied or pending entry(MSW-609)
    Given define template request form and remember user and company bills: <type> entry
     And get csrf token
    When make post request
     And pause - 2 sec(s)
     And get user and company bills before canceling entry
    Then cancel the created <type> entry
     And pause - 2 sec(s)
     And get user and company bills after canceling entry
     And check status of task
     And pause - 2 sec(s)
     And check canceling of entry and transactions
     And check user and company bills after canceling <type> entry
      Examples:
        |  type   |
        | applied |
        | pending |


  Scenario Outline: checking filters of REPORTS
    Given get user bills for reports
     And get report_fields
     And formation of url for report: <filter> with actual date
    When [AS] download report xlsx
    Then [AS] compare xlsx with api results
    Examples: filter
        |  filter   |
        |  user     |
        |  account  |
        |  field    |











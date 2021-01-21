@fin_user
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
        |  transaction_out.user_bill      | null              |  One side of Entry are required!                                        |

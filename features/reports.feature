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


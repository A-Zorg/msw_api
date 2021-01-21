Feature:  reconciliation check access

    Scenario Outline: not authenticated user
      Given alien makes <method> request: <url>
      Then check response of request: Authentication credentials were not provided. is <bool>

      Examples: cases
      | url                                      | method          | bool |
      | /reconciliation/                         | get             | True |
      | /reconciliation/                         | post            | True |
      | /reconciliation/all_users_data/          | get             | True |
      | /reconciliation/all_users_data/xlsx      | get             | True |
      | /reconciliation/date_of_reconciliation/  | post            | True |
      | /reconciliation/feedback/                | post            | True |
      | /reconciliation/import_hr/               | get             | True |
      | /reconciliation/questions/               | post            | True |
      | /reconciliation/reports_update/          | get             | True |
      | /reconciliation/reports_update/          | post            | True |
      | /reconciliation/services_compensations/  | post            | True |
      | /reconciliation/services_compensations/  | get             | True |
      | /reconciliation/status/                  | get             | True |
      | /reconciliation/status/                  | post            | True |
      | /reconciliation/status_accounts/         | get             | True |
      | /reconciliation/user_data/               | get             | True |


    Scenario Outline: manager user
      Given manager makes <method> request: <url>
      Then check response of request: You do not have permission to perform this action. is <bool>

      Examples: cases
      | url                                      | method          | bool  |
      | /reconciliation/                         | get             | False |
      | /reconciliation/                         | post            | False |
      | /reconciliation/all_users_data/          | get             | True  |
      | /reconciliation/all_users_data/xlsx      | get             | True  |
      | /reconciliation/date_of_reconciliation/  | get             | True  |
      | /reconciliation/feedback/                | post            | False |
      | /reconciliation/import_hr/               | get             | True  |
      | /reconciliation/questions/               | post            | False |
      | /reconciliation/reports_update/          | get             | True  |
      | /reconciliation/services_compensations/  | get             | True  |
      | /reconciliation/status/                  | get             | False |
      | /reconciliation/status/                  | post            | True  |
      | /reconciliation/status_accounts/         | get             | True  |
      | /reconciliation/user_data/               | get             | False |



    Scenario Outline: risk user
      Given risk makes <method> request: <url>
      Then check response of request: You do not have permission to perform this action. is <bool>

      Examples: cases
      | url                                      | method          | bool  |
      | /reconciliation/                         | get             | False |
      | /reconciliation/                         | post            | False |
      | /reconciliation/all_users_data/          | get             | False |
      | /reconciliation/all_users_data/xlsx      | get             | False |
      | /reconciliation/date_of_reconciliation/  | get             | False |
      | /reconciliation/feedback/                | post            | False |
      | /reconciliation/import_hr/               | get             | False |
      | /reconciliation/questions/               | post            | False |
      | /reconciliation/reports_update/          | get             | False |
      | /reconciliation/services_compensations/  | get             | False |
      | /reconciliation/status/                  | get             | False |
      | /reconciliation/status/                  | post            | False |
      | /reconciliation/status_accounts/         | get             | False |
      | /reconciliation/user_data/               | get             | False |






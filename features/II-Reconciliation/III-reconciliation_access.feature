Feature:  reconciliation check access
#
#    Scenario Outline: not authenticated user
#      Then alien makes request: <url> , result: <code>
#
#      Examples: cases
#      | url                                      | code |
#      | /reconciliation/                         | 403  |
#      | /reconciliation/3/                       | 403  |
#      | /reconciliation/all_users_data/          | 403  |
#      | /reconciliation/all_users_data/xlsx      | 403  |
#      | /reconciliation/date_of_reconciliation/  | 403  |
#      | /reconciliation/feedback/                | 403  |
#      | /reconciliation/import_hr/               | 403  |
#      | /reconciliation/questions/               | 403  |
#      | /reconciliation/reports_update/          | 403  |
#      | /reconciliation/reports_update/          | 403  |
#      | /reconciliation/services_compensations/  | 403  |
#      | /reconciliation/services_compensations/  | 403  |
#      | /reconciliation/status/                  | 403  |
#      | /reconciliation/status/                  | 403  |
#      | /reconciliation/status_accounts/         | 403  |
#      | /reconciliation/user_data/               | 403  |
#      | /reconciliation/user_data/3/             | 403  |
#
#
#    Scenario Outline: manager user
#      Given manager makes <method> request: <url>
#      Then check response of request: You do not have permission to perform this action. is <bool>
#
#      Examples: cases
#      | url                                      | method          | bool  |
#      | /reconciliation/                         | get             | False |
#      | /reconciliation/                         | post            | False |
#      | /reconciliation/3/                       | get             | True  |
#      | /reconciliation/all_users_data/          | get             | True  |
#      | /reconciliation/all_users_data/xlsx      | get             | True  |
#      | /reconciliation/date_of_reconciliation/  | get             | True  |
#      | /reconciliation/feedback/                | post            | False |
#      | /reconciliation/import_hr/               | get             | True  |
#      | /reconciliation/questions/               | post            | False |
#      | /reconciliation/reports_update/          | get             | True  |
#      | /reconciliation/services_compensations/  | get             | True  |
#      | /reconciliation/status/                  | get             | False |
#      | /reconciliation/status/                  | post            | True  |
#      | /reconciliation/status_accounts/         | get             | True  |
#      | /reconciliation/user_data/               | get             | False |
#      | /reconciliation/user_data/3/             | get             | True  |
#
#
#
#    Scenario Outline: risk user
#      Given risk makes <method> request: <url>
#      Then check response of request: You do not have permission to perform this action. is <bool>
#
#      Examples: cases
#      | url                                      | method          | bool  |
#      | /reconciliation/                         | get             | False |
#      | /reconciliation/                         | post            | False |
#      | /reconciliation/3/                       | get             | False |
#      | /reconciliation/3/                       | post            | False |
#      | /reconciliation/all_users_data/          | get             | False |
#      | /reconciliation/all_users_data/xlsx      | get             | False |
#      | /reconciliation/date_of_reconciliation/  | get             | False |
#      | /reconciliation/feedback/                | post            | False |
#      | /reconciliation/import_hr/               | get             | False |
#      | /reconciliation/questions/               | post            | False |
#      | /reconciliation/reports_update/          | get             | False |
#      | /reconciliation/services_compensations/  | get             | False |
#      | /reconciliation/status/                  | get             | False |
#      | /reconciliation/status/                  | post            | False |
#      | /reconciliation/status_accounts/         | get             | False |
#      | /reconciliation/user_data/               | get             | False |
#      | /reconciliation/user_data/3/             | get             | False |
#
#
#



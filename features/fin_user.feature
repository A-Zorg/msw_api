@fin_user
Feature: FIN permissions

  Scenario Outline: FIN permissions
    Then check staff permissions for AS: <url> and <success>
    Examples: urls
        |  url                                  |success|
        |  /accounting_system/agents_create/    | True  |
        |  /accounting_system/bills/company/    | True  |
        |  /accounting_system/bills/user/types/ | True  |
        |  /accounting_system/bills/user/1/     | True  |
        |  /accounting_system/bills/users/      | True  |
        |  /accounting_system/entries/          | True  |
        |  /accounting_system/entry/            | False |
        |  /accounting_system/report_fields/    | True  |
        |  /accounting_system/report/           | True  |

  Scenario: check company bills list
    Then check company bills list

  Scenario: check user bills list
    Then check user bills list

  Scenario: check users bills
    Then check users bills
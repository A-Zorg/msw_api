@super_user
Feature: super_user permissions

  Scenario Outline: super_user permissions
    Then check super_user permissions for AS: <url> and <success>
    Examples: urls
        |  url                                  |success |
        |  /accounting_system/agents_create/    | True   |
        |  /accounting_system/bills/company/    | False  |
        |  /accounting_system/bills/user/types/ | False  |
        |  /accounting_system/bills/user/1/     | False  |
        |  /accounting_system/bills/users/      | False  |
        |  /accounting_system/entries/          | False  |
        |  /accounting_system/entry/            | True   |
        |  /accounting_system/report_fields/    | False  |
        |  /accounting_system/report/           | False  |
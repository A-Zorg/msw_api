@fin_user
Feature: FIN permissions

  Scenario Outline: FIN permissions
    Then fin makes request: <url> , result: <code>
    Examples: urls
        |  url                                            | code |
        |  /accounting_system/bills/company/              | 200  |
        |  /accounting_system/bills/user/types/           | 200  |
        |  /accounting_system/bills/user/1/               | 200  |
        |  /accounting_system/bills/users/                | 200  |
        |  /accounting_system/entries/                    | 200  |
        |  /accounting_system/entry/                      | 403  |
        |  /accounting_system/entry/cancel/1/             | 403  |
        |  /accounting_system/entry/custom/net_buyout/    | 403  |
        |  /accounting_system/entry/multiple_transactions/| 403  |
        |  /accounting_system/report_fields/              | 200  |
        |  /accounting_system/report/                     | 200  |
        |  /accounting_system/account_type/               | 200  |
        |  /accounting_system/account_type/broker/        | 200  |
        |  /accounting_system/account_type/clearing/      | 200  |
        |  /accounting_system/account_type/company/       | 200  |


  Scenario: check company bills list
    Then check company bills list

  Scenario: check user bills list
    Then check user bills list

  Scenario: check users bills
    Then check users bills


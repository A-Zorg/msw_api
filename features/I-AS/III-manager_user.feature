@manager_user
Feature: no permission


  Scenario Outline: check manager permissions
    Then manager makes request: <url> , result: <code>
    Examples: urls
        |  url                                            |code  |
        |  /accounting_system/bills/company/              | 403  |
        |  /accounting_system/bills/user/types/           | 200  |
        |  /accounting_system/bills/user/1/               | 403  |
        |  /accounting_system/bills/users/                | 403  |
        |  /accounting_system/entries/                    | 403  |
        |  /accounting_system/entry/                      | 403  |
        |  /accounting_system/entry/cancel/1/             | 403  |
        |  /accounting_system/entry/custom/net_buyout/    | 403  |
        |  /accounting_system/entry/multiple_transactions/| 403  |
        |  /accounting_system/report_fields/              | 200  |
        |  /accounting_system/report/                     | 200  |
        |  /accounting_system/account_type/               | 403  |
        |  /accounting_system/account_type/broker/        | 200  |
        |  /accounting_system/account_type/clearing/      | 403  |
        |  /accounting_system/account_type/company/       | 403  |
        |  /accounting_system/accounting/3/               | 200  |
        |  /accounting_system/accounting/history/xlsx_account/       | 200   |
        |  /accounting_system/accounting/history/xlsx_payment_queue/ | 200   |





Feature: check ACCOUNTING access

    Scenario Outline: checking credentials for none authenticated
    Then alien makes request: <url> , result: <code>
    Examples: urls
        |  url                                          | code  |
        |  /accounting/account_data/                    | 403   |
        |  /accounting/accounts_upload/                 | 200   |
        |  /accounting/data_history/xlsx_account/       | 403   |
        |  /accounting/data_history/xlsx_payment_queue/ | 403   |
        |  /accounting/payment_queue_data/              | 403   |


    Scenario Outline: checking credentials for manager
    Then manager makes request: <url> , result: <code>
    Examples: urls
        |  url                                          | code  |
        |  /accounting/account_data/                    | 200   |
        |  /accounting/accounts_upload/                 | 200   |
        |  /accounting/data_history/xlsx_account/       | 200   |
        |  /accounting/data_history/xlsx_payment_queue/ | 200   |
        |  /accounting/payment_queue_data/              | 200   |

  
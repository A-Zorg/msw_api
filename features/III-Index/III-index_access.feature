Feature:  check "Index" access

  Scenario Outline: checking credentials for none authenticated
    Then alien makes request: <url> , result: <code>
    Examples: urls
        |  url                            | code  |
        |  /index/books/                  | 403   |
        |  /index/books/categories/       | 403   |
        |  /index/contests/               | 403   |
        |  /index/holidays/               | 403   |
        |  /index/my_books/               | 403   |
        |  /index/news/                   | 403   |
        |  /index/news/1/likes/           | 403   |
        |  /index/news/1/views/           | 403   |
        |  /index/users/                  | 403   |
        |  /index/services_compensations/ | 403   |
        | /media/contest/image_upload     | 200   |
        |  /media/contest/top30/button    | 403   |
        |  /media/contest/top30/image     | 403   |
        |  /media/news/1                  | 403   |

  Scenario Outline: checking credentials for manager
    Then manager makes request: <url> , result: <code>
    Examples: urls
        |  url                            | code  |
        |  /index/books/                  | 200   |
        |  /index/books/categories/       | 200   |
        |  /index/contests/               | 200   |
        |  /index/holidays/               | 200   |
        |  /index/my_books/               | 200   |
        |  /index/news/                   | 200   |
        |  /index/news/1/likes/           | 200   |
        |  /index/news/1/views/           | 200   |
        |  /index/users/                  | 403   |
        |  /index/services_compensations/ | 200   |
        | /media/contest/image_upload     | 200   |
        |  /media/contest/top30/button    | 200   |
        |  /media/contest/top30/image     | 200   |
        |  /media/news/1                  | 200   |


    Scenario Outline: checking credentials for risk
    Then fin makes request: <url> , result: <code>
    Examples: urls
        |  url                            | code  |
        |  /index/books/                  | 200   |
        |  /index/books/categories/       | 200   |
        |  /index/contests/               | 200   |
        |  /index/holidays/               | 200   |
        |  /index/my_books/               | 200   |
        |  /index/news/                   | 200   |
        |  /index/news/1/likes/           | 200   |
        |  /index/news/1/views/           | 200   |
        |  /index/users/                  | 200   |
        |  /index/services_compensations/ | 200   |
        | /media/contest/image_upload     | 200   |
        |  /media/contest/top30/button    | 200   |
        |  /media/contest/top30/image     | 200   |
        |  /media/news/1                  | 200   |
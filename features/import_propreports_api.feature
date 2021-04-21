Feature: import from propreports_api


 Scenario Outline: check propreports_api_daily_import
    Given get random ticker (review_date==2020-08-18)
     And get from db first DR_data_tuple: request_#==1, review_date==2020-08-18
     And get from db second DR_data_dictionary: request_#==2, review_date==2020-08-18
    Then [DR] check calculation: avg_price ans real in PropreportsData






      #    Given from propreports get data of selected account for selected data
#     And parse data from xls file
#     And clear review_propreportsdata db table for selected data
#     And run propreports_api_daily_import for selected data
#     And wait for task is finished: propreports_api_daily_import
#    When from db get data of selected account for selected data
#    Then compare data from propreports and db
      Examples:
        | acc_name     | acc_regex            | action_1 |
        | SMRT056 asd  | ^SMRT[0-9]{3}$       | presence |
#        | STSTRADER023 | ^STSTRADER[0-9]{3}$  | presence |
#        | SMRT003NT 12 | ^SMRT[0-9]{3}N(T)?$  | presence |
#        | STS343       | ^STS[0-9]{3}$        | presence |
#        | STS343N a4d  | ^STS[0-9]{3}N(T)?$   | presence |
#        | EQS023 asd   | ^EQS[0-9]{3}$        | presence |
#        | EQS023N asd  | ^EQS[0-9]{3}N(T)?$   | presence |
#        | 34504123     | ^34504[0-9]{3}$      | presence |
#        | 34546789 af  | ^3454[0-9]{4}$       | presence |
#        | EQS023Nasd   | ^EQS[0-9]{3}$        | absence  |
#        | wqeEQS023N   | ^EQS[0-9]{3}$        | absence  |
#        | 12345678     | ^3454[0-9]{4}$       | absence  |

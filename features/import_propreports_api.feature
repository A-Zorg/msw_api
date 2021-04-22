Feature: import from propreports_api


 Scenario: check propreports_api_daily_import
    Given get random ticker (review_date==2020-08-18)
     And get from db first DR_data_tuple: request_#==1, review_date==2020-08-18
     And get from db second DR_data_dictionary: request_#==2, review_date==2020-08-18
    Then [DR] check calculation: avg_price ans real in PropreportsData
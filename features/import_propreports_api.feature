Feature: import from propreports_api

  @autorepeat @2
 Scenario: check calculation avg_price and real or premarket data
    Given get random ticker (review_date==2020-08-18)
     And get from db first DR_data_tuple: request_#==1, review_date==2020-08-18
     And get from db second DR_data_dictionary: request_#==2, review_date==2020-08-18
    Then [DR] check calculation: avg_price ans real in PropreportsData

 @autorepeat @2
 Scenario: check calculation avg_price and real or intraday data
    Given get random ticker (review_date==2020-08-18)
     And get from db first DR_data_tuple: request_#==3, review_date==2020-08-18
     And get from db second DR_data_dictionary: request_#==4, review_date==2020-08-18
    Then [DR] check calculation: avg_price ans real in PropreportsData

 @autorepeat @3
 Scenario: check calculation avg_price and real or postmarket data
    Given get random ticker (review_date==2020-08-18)
     And get from db first DR_data_tuple: request_#==5, review_date==2020-08-18
     And get from db second DR_data_dictionary: request_#==6, review_date==2020-08-19
    Then [DR] check calculation: avg_price ans real in PropreportsData

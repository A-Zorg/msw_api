Feature: import from propreports_api

  @autorepeat @10
  Scenario: check unrealizedpertickeraccount postmarket data
    Given get random ticker
     And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==POS
     And from db get second DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==POS
     And from db get third DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==INT
    Then [DR] check calculation: unrealizedpertickeraccount

  @autorepeat @10
  Scenario: check unrealizedpertickeraccount intraday data
    Given get random ticker
    And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==next_date, session==INT
     And from db get second DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==next_date, session==INT
     And from db get third DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==PRE
    Then [DR] check calculation: unrealizedpertickeraccount

  @autorepeat @10
  Scenario: check unrealizedpertickeraccount premarket data
    Given get random ticker
    And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==PRE
     And from db get second DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==PRE
     And from db get third DR_data_dictionary: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==POS
    Then [DR] check calculation: unrealizedpertickeraccount

   @autorepeat @10
   Scenario: check unrealizedperticker premarket data
      Given get random ticker
       And from db get first DR_data_dictionary: request_name==unrealizedpertickeraccount, review_date==target_date, session==PRE
       And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==target_date, session==PRE
      Then [DR] check calculation: unrealizedperticker

   @autorepeat @10
   Scenario: check unrealizedperticker intraday data
      Given get random ticker
       And from db get first DR_data_dictionary: request_name==unrealizedpertickeraccount, review_date==target_date, session==INT
       And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==target_date, session==INT
      Then [DR] check calculation: unrealizedperticker

#   @autorepeat @10
#   Scenario: check unrealizedperticker postmarket data
#      Given get random ticker
#       And from db get first DR_data_dictionary: request_name==unrealizedpertickeraccount, review_date==target_date, session==POS
#       And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==target_date, session==POS
#      Then [DR] check calculation: unrealizedperticker
#
#
#
#
#








Feature: calculation interval_per_ticker

  @autorepeat @20
  Scenario: check calculation of intervalsperticker premarket
    Given get random ticker
     And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==PRE
     And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==target_date, session==POS
     And from db get third DR_data_dictionary: request_name==intervalsperticker, review_date==target_date, session==PRE
    Then [DR] check calculation: intervalsperticker(PRE)

  @autorepeat @20
  Scenario: check calculation of intervalsperticker intraday
    Given get random ticker
     And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==INT
     And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==prev_date, session==PRE
     And from db get third DR_data_dictionary: request_name==intervalsperticker, review_date==target_date, session==INT
    Then [DR] check calculation: intervalsperticker(INT)

  @autorepeat @20
  Scenario: check calculation of intervalsperticker postmarket
    Given get random ticker
     And from db get first DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==POS
     And from db get second DR_data_dictionary: request_name==unrealizedperticker, review_date==target_date, session==INT
     And from db get third DR_data_dictionary: request_name==intervalsperticker, review_date==target_date, session==POS
    Then [DR] check calculation: intervalsperticker(POS)
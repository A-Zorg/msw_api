Feature: calculation datepertickeraccount and dataperticker


  @autorepeat @10
  Scenario: check calculation of datepertickeraccount premarket
    Given get random ticker
     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==PRE
     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==PRE
    Then [DR] check calculation: datepertickeraccount

  @autorepeat @10
  Scenario: check calculation of datepertickeraccount intraday
    Given get random ticker
     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==INT
     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==INT
    Then [DR] check calculation: datepertickeraccount

  @autorepeat @10
  Scenario: check calculation of datepertickeraccount postmarket
    Given get random ticker
     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==POS
     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==POS
    Then [DR] check calculation: datepertickeraccount


  @autorepeat @10
  Scenario: check calculation of dateperticker premarket(result, shares_traded, result_in_points)
    Given get random ticker
     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==POS
     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==POS
    Then [DR] check calculation: dateperticker(result, shares_traded, result_in_points)

  @autorepeat @10
  Scenario: check calculation of dateperticker premarket(result, shares_traded, result_in_points)
    Given get random ticker
     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==INT
     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==INT
    Then [DR] check calculation: dateperticker(result, shares_traded, result_in_points)

  @autorepeat @100
  Scenario: check calculation of dateperticker premarket(result, shares_traded, result_in_points)
    Given get random ticker
     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==PRE
     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==PRE
    Then [DR] check calculation: dateperticker(result, shares_traded, result_in_points)



  @autorepeat @10
  Scenario: check calculation of dateperticker nonmarket(result, shares_traded, result_in_points)
    Given get random ticker
     And from db get first DR_data_tuple: request_name==dataperticker, review_date==target_date, session==PRE
     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==POS
     And from db get third DR_data_tuple: request_name==dataperticker, review_date==target_date, session==NON
    Then [DR] check calculation: dateperticker NON(result, shares_traded, result_in_points)

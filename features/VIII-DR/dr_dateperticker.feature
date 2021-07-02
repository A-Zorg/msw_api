Feature: calculation datepertickeraccount and dataperticker

#  @autorepeat @20
#  Scenario: check calculation of datepertickeraccount premarket
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==PRE
#     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==PRE
#    Then [DR] check calculation: datepertickeraccount
#
#  @autorepeat @20
#  Scenario: check calculation of datepertickeraccount intraday
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==INT
#     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==INT
#    Then [DR] check calculation: datepertickeraccount
#
#  @autorepeat @20
#  Scenario: check calculation of datepertickeraccount postmarket
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==propreportsdata_pertickeraccount, review_date==target_date, session==POS
#     And from db get second DR_data_tuple: request_name==datapertickeraccount_2, review_date==target_date, session==POS
#    Then [DR] check calculation: datepertickeraccount
#
#  @autorepeat @20
#  Scenario: check calculation of dateperticker postmarket(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==POS
#     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==POS
#    Then [DR] check calculation: dateperticker:POS (result, shares_traded, result_in_points)
#
#  @autorepeat @20
#  Scenario: check calculation of dateperticker intraday(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==INT
#     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==INT
#    Then [DR] check calculation: dateperticker:INT (result, shares_traded, result_in_points)
#
#  @autorepeat @20
#  Scenario: check calculation of dateperticker premarket(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==datapertickeraccount_1, review_date==target_date, session==PRE
#     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==PRE
#    Then [DR] check calculation: dateperticker:PRE (result, shares_traded, result_in_points)
#
#  @autorepeat @20
#  Scenario: check calculation of dateperticker nonmarket(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker, review_date==target_date, session==PRE
#     And from db get second DR_data_tuple: request_name==dataperticker, review_date==target_date, session==POS
#     And from db get third DR_data_tuple: request_name==dataperticker, review_date==target_date, session==NON
#    Then [DR] check calculation: dateperticker NON(result, shares_traded, result_in_points)
#
#  @autorepeat @20
#  Scenario: check nonmarket(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker, review_date==target_date, session==NON
#     And from db get second DR_data_tuple: request_name==unrealizedperticker, review_date==target_date, session==INT
#     And from db get third DR_data_tuple: request_name==intervalsperticker_non, review_date==target_date, session==NON
#    Then [DR] check max_pos for NON
#
#  @autorepeat @20
#  Scenario: check nonmarket(result, shares_traded, result_in_points)
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker, review_date==next_date, session==INT
#     And from db get second DR_data_tuple: request_name==unrealizedperticker, review_date==target_date, session==PRE
#     And from db get third DR_data_tuple: request_name==intervalsperticker_int, review_date==next_date, session==INT
#    Then [DR] check max_pos for INT

Feature: calculation datapersession



#  Scenario: check calculation of datapersession premarket
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker_shares_traded, review_date==target_date, session==PRE
#     And from db get second DR_data_tuple: request_name==dataperticker_pos_result, review_date==target_date, session==PRE
#     And from db get third DR_data_tuple: request_name==dataperticker_neg_result, review_date==target_date, session==PRE
#     And from db get forth DR_data_dictionary: request_name==datapersession, review_date==target_date, session==PRE
#    Then [DR] check calculation: datapersession
#
#  Scenario: check calculation of datapersession intraday
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker_shares_traded, review_date==target_date, session==INT
#     And from db get second DR_data_tuple: request_name==dataperticker_pos_result, review_date==target_date, session==INT
#     And from db get third DR_data_tuple: request_name==dataperticker_neg_result, review_date==target_date, session==INT
#     And from db get forth DR_data_dictionary: request_name==datapersession, review_date==target_date, session==INT
#    Then [DR] check calculation: datapersession
#
#  Scenario: check calculation of datapersession postmarket
#    Given get random ticker
#     And from db get first DR_data_tuple: request_name==dataperticker_shares_traded, review_date==target_date, session==POS
#     And from db get second DR_data_tuple: request_name==dataperticker_pos_result, review_date==target_date, session==POS
#     And from db get third DR_data_tuple: request_name==dataperticker_neg_result, review_date==target_date, session==POS
#     And from db get forth DR_data_dictionary: request_name==datapersession, review_date==target_date, session==POS
#    Then [DR] check calculation: datapersession
#

#  @autorepeat @10
#  Scenario: check calculation of dateperticker premarket(result_in_percents, office_volume)
#    Given get random ticker
#     And from db get first DR_data_dictionary: request_name==datapersession, review_date==target_date, session==PRE
#     And from db get second DR_data_dictionary: request_name==dataperticker_all, review_date==target_date, session==PRE
#    Then [DR] check calculation: dateperticker(result_in_percents, office_volume)

#  @autorepeat @10
#  Scenario: check calculation of dateperticker intraday(result_in_percents, office_volume)
#    Given get random ticker
#     And from db get first DR_data_dictionary: request_name==datapersession, review_date==target_date, session==INT
#     And from db get second DR_data_dictionary: request_name==dataperticker_all, review_date==target_date, session==INT
#    Then [DR] check calculation: dateperticker(result_in_percents, office_volume)

#  @autorepeat @10
#  Scenario: check calculation of dateperticker postmarket(result_in_percents, office_volume)
#    Given get random ticker
#     And from db get first DR_data_dictionary: request_name==datapersession, review_date==target_date, session==POS
#     And from db get second DR_data_dictionary: request_name==dataperticker_all, review_date==target_date, session==POS
#    Then [DR] check calculation: dateperticker(result_in_percents, office_volume)
#
#  @autorepeat @10
#  Scenario: check calculation of dateperticker postmarket(result_in_percents, office_volume)
#    Given get random ticker
#     And from db get first DR_data_dictionary: request_name==datapersession, review_date==target_date, session==NON
#     And from db get second DR_data_dictionary: request_name==dataperticker_all, review_date==target_date, session==NON
#    Then [DR] check calculation: dateperticker(result_in_percents, office_volume)

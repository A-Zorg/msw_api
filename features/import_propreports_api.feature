Feature: import from propreports_api

#  @autorepeat @2
# Scenario: check calculation avg_price and real or premarket data
#    Given get random ticker (review_date==2020-08-18)
#     And get from db first DR_data_tuple: request_#==1, review_date==2020-08-18
#     And get from db second DR_data_dictionary: request_#==2, review_date==2020-08-18
#    Then [DR] check calculation: avg_price ans real in PropreportsData

# @autorepeat @2
# Scenario: check calculation avg_price and real or intraday data
#    Given get random ticker (review_date==2020-08-18)
#     And get from db first DR_data_tuple: request_#==3, review_date==2020-08-18
#     And get from db second DR_data_dictionary: request_#==4, review_date==2020-08-18
#    Then [DR] check calculation: avg_price ans real in PropreportsData
#
# @autorepeat @3
# Scenario: check calculation avg_price and real or postmarket data
#    Given get random ticker (review_date==2020-08-18)
#     And get from db first DR_data_tuple: request_#==5, review_date==2020-08-18
#     And get from db second DR_data_dictionary: request_#==6, review_date==2020-08-19
#    Then [DR] check calculation: avg_price ans real in PropreportsData
#
# @autorepeat @5
# Scenario: check calculation total_real, total_shares_traded (review_datapertickeraccount)
#   Given get random account (review_date: 2020-08-18, session: PRE)
#     And get actual data from review_datapertickeraccount
#    Then check calculation: total_real, total_shares_traded
#
# @autorepeat @5
#Scenario: check calculation total_real, total_shares_traded (review_datapertickeraccount)
#   Given get random account (review_date: 2020-08-18, session: INT)
#     And get actual data from review_datapertickeraccount
#    Then check calculation: total_real, total_shares_traded
#
# @autorepeat @5
#Scenario: check calculation total_real, total_shares_traded (review_datapertickeraccount)
#   Given get random account (review_date: 2020-08-18, session: POS)
#     And get actual data from review_datapertickeraccount
#    Then check calculation: total_real, total_shares_traded
#
# @autorepeat @1
# Scenario: check calculation total_real, total_shares_traded, max_pos (review_dataperticker)
#   Given save input data (review_date: 2020-08-18, session: PRE)
#     And get actual data from review_dataperticker
#    Then check calculation: total_real, total_shares_traded, max_pos
#
# @autorepeat @1
# Scenario: check calculation total_real, total_shares_traded, max_pos (review_dataperticker)
#   Given save input data (review_date: 2020-08-18, session: INT)
#     And get actual data from review_dataperticker
#    Then check calculation: total_real, total_shares_traded, max_pos
#
# @autorepeat @1
# Scenario: check calculation total_real, total_shares_traded, max_pos (review_dataperticker)
#   Given save input data (review_date: 2020-08-18, session: POS)
#     And get actual data from review_dataperticker
#    Then check calculation: total_real, total_shares_traded, max_pos
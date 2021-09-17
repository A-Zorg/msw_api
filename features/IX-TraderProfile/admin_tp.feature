Feature: Admin TP


#  Scenario: Check RB2 period functionality
#    Given Delete manager's row from RiskBlockPeriod table
#    When Make PUT request to api/trader/risk_block2_period/ by admin
#    Then Check created RiskBlockPeriod row
#

#  Scenario Outline: Check log status
#    Given Create user's logs: <condition>
#    Then Log-status of user should be <result>
#    Examples:
#        | condition                   | result   |
#        | two actual                  | not null |
#        | two expired                 | null     |
#        | one expired and one actual  | null or not |

#
#  Scenario: Check main-info endpoint
#    Given get user's data from DB
#    When get user's data through api/trader/main_info/
#    Then Main-info: compare actual and expected data


#  Scenario: 123123
#    Given sjdhgfjshdgf


#    Scenario: hr block
#    Given get user's data from smartbase
##

#    Scenario: last performance block
#     Given Get expected last performance block data
#

#    Scenario: propreports block
#     Given Get expected propreports block data

#         Scenario: risk 1 block
#     Given Get expected risk block 1 data
#
#
#           Scenario: performance chart
#     Given Get performance chart data


#
#           Scenario: risk 2 block
#     Given Get expected risk block 2 data as risk

      Scenario Outline: risk 3 block
        Given Create user's logs: <condition>
        When Get expected risk block 3 data
        Examples:
        | condition                   |
        | two actual                  |
        | two expired                 |
        | one expired and one actual  |
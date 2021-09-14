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


  Scenario: Check main-info endpoint
    Given get user's data from DB
    When get user's data through api/trader/main_info/
    Then Main-info: compare actual and expected data
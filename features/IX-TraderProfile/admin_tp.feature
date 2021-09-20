Feature: Admin TP

   Scenario: Check RB2 period functionality
    Given Delete manager's row from RiskBlockPeriod table
    When Make PUT request to api/trader/risk_block2_period/ by admin
    Then Check created RiskBlockPeriod row


   Scenario Outline: Check log status
    Given Create user's logs: <condition>
    Then Log-status of user should be <result>
    Examples:
        | condition                   | result   |
        | two actual                  | not null |
        | two expired                 | null     |
        | one expired and one actual  | null or not |


   Scenario: Check main-info endpoint
    Given get user's data from DB
    When get user's data through api/trader/main_info/
    Then Main-info: compare actual and expected data


   Scenario: Primary risk block
    Given get expected PRIMARY RISK BLOCK data of user: 193
    When get actual PRIMARY RISK BLOCK data of user: 193
    Then PRIMARY RISK BLOCK: compare actual and expected data


   Scenario: hr block
    Given get user's HR BLOCK data from smartbase
    When get actual HR BLOCK data
    Then HR BLOCK: compare actual and expected data


    Scenario: last performance block
     Given get expected LAST PERFORMANCE BLOCK data of user: 193
     When get actual LAST PERFORMANCE BLOCK data of user: 193
     Then LAST PERFORMANCE BLOCK: compare actual and expected data


    Scenario: propreports block
     Given get expected PROPREPORTS BLOCK data of user: 90001
     When get actual PROPREPORTS BLOCK data of user: 90001
     Then PROPREPORTS BLOCK: compare actual and expected data

     Scenario: RISK BLOCK I
      Given get expected RISK BLOCK I data of user: 90001
      When get actual RISK BLOCK I data of user: 90001
      Then RISK BLOCK I: compare actual and expected data


     Scenario: PERFORMANCE CHART block
      Given get PERFORMANCE CHART data of user: 172
      When get actual PERFORMANCE CHART data of user: 172
      Then PERFORMANCE CHART: compare actual and expected data



     Scenario: RISK BLOCK II
      Given get expected RISK BLOCK II of user: 172 data as risk
      When get actual RISK BLOCK II data of user: 172
      Then RISK BLOCK II: compare actual and expected data


      Scenario Outline: RISK BLOCK III
        Given Create user's logs: <condition>
         And get expected RISK BLOCK III data
        When get actual RISK BLOCK III data
        Then RISK BLOCK III: compare actual and expected data
        Examples:
        | condition                   |
        | two actual                  |
        | two expired                 |
        | one expired and one actual  |
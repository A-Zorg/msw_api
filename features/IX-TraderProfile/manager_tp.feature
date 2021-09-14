Feature: Manager TP

#  Scenario: Check layout functionality
#    Given Delete manager's row from TraderProfile table
#    When Make PUT request to api/trader/layout/ by manager
#    Then Check created TraderProfile row: api/trader/layout/

  Scenario: Check RB2 period functionality
    Given Delete manager's row from TraderProfile table
    When Make PUT request to api/trader/risk_block2_period/ by manager
    Then Check created TraderProfile row: api/trader/risk_block2_period/

  Scenario: Check trader_info endpoint: api/trader/main_info/136/
    Given asdasdasd
#    When Make PUT request to api/trader/risk_block2_period/ by manager
#    Then Check created TraderProfile row: api/trader/risk_block2_period/
Feature: check "login"

  Scenario: logout-login cycle
    Given logout manager
     And get login token for authentication
     And perform login by manager
     And get 2fa token for authentication
    When pause - 32 sec(s)
    Then perform token auth. by manager


  Scenario: change password
    Given alien get login token for authentication
     And send message to the manager's email
     And pause - 5 sec(s)
     And get "change password" key in Riskbot
    When change username and password to new
     And send message to the manager's email
     And pause - 5 sec(s)
     And get "change password" key in email
    Then change username and password to old



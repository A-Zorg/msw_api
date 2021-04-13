@fin_user
Feature: AS updates


  Scenario Outline: JE
    Given get user and company bill_id
#     And create PROPREPORTS entries:-Nomura-, -EQS-, -Broker 5-, -1-, -123-
#     And create PROPREPORTS entries:-Nomura-, -SMRT-, -Broker 5-, -0-, --45.34-
#     And create PROPREPORTS entries:-default-, -STS-, -Broker 5-, -1-, -99.1234-
#     And create PROPREPORTS entries:-default-, -EQS-, -Takion-, -0-, -0.9999-
#     And create PROPREPORTS entries:-default-, -STS-, -Takion-, -1-, -122143-
#     And create PROPREPORTS entries:-default-, -EQS-, -Broker 4-, -0-, --333.333-
     And fin_user get broker list
     And fin_user get clearing list
     And fin_user get company list
     And get user bills
     And create url with filters: <company>, <broker>, <clearing>
    When by FIN create journal entries report
    Then check actual result of JE report with expected: <result>

      Examples:
        |  company  | broker    | clearing | result    |
        |  all      | Broker 5  |   all    | 176.7834  |

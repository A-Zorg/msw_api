@super_user
Feature:  entries


  Scenario Outline: creation of past entries
    Given get user number bills
     And get company number bills
     And define request form
     And random amount pick
     And random choice TRANSACTION FROM <from> bill
     And random choice TRANSACTION TO <to> bill
     And get of PAST date
     And get csrf token
    When make post request to create entry
     And pause - 5 sec(s)
    Then check status of entry: applied
          Examples: forward
        |  from     |to     |
        |  company  |user   |
        |  company  |company|
        |  user     |user   |
        |  user     |company|

  Scenario Outline: creation of future entries
    Given get user number bills
     And get company number bills
     And define request form
     And random amount pick
     And random choice TRANSACTION FROM <from> bill
     And random choice TRANSACTION TO <to> bill
     And get of FUTURE date
     And get csrf token
    When make post request to create entry
    Then check status of entry: pending
     And pause - 15 sec(s)
     But check status of entry: applied
          Examples: forward
        |  from     |to     |
        |  company  |user   |
        |  company  |company|
        |  user     |user   |
        |  user     |company|


  Scenario Outline: creation of past mass transaction
    Given get user number bills
     And get company number bills
     And define request form of mass transaction
     And get random amount of mass transaction
     And random choice of MASS TRANSACTION <curr_1> users bills
     And random choice of MASS TRANSACTION <curr_2> company bill
     And get of PAST date of mass transaction
    When make post request to create mass transaction
     And pause - 5 sec(s)
    Then check status of entry: applied
          Examples: forward
        |  curr_1     |  curr_2   |
        |  FROM       |  TO       |
        |  FROM       |  TO       |

  Scenario Outline: creation of future mass transaction
    Given get user number bills
     And get company number bills
     And define request form of mass transaction
     And get random amount of mass transaction
     And random choice of MASS TRANSACTION <curr_1> users bills
     And random choice of MASS TRANSACTION <curr_2> company bill
     And get of FUTURE date of mass transaction
    When make post request to create mass transaction
    Then check status of entry: pending
     And pause - 15 sec(s)
     But check status of entry: applied
          Examples: forward
        |  curr_1     |  curr_2   |
        |  FROM       |  TO       |
        |  FROM       |  TO       |

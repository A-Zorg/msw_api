@super_user
Feature: journal entries


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

#  Scenario Outline: creation of future entries
#    Given get user number bills
#     And get company number bills
#     And define request form
#     And random amount pick
#     And random choice TRANSACTION FROM <from> bill
#     And random choice TRANSACTION TO <to> bill
#     And get of FUTURE date
#     And get csrf token
#    When make post request to create entry
#    Then check status of entry: pending
#     And pause - 70 sec(s)
#     But check status of entry: applied
#          Examples: forward
#        |  from     |to     |
#        |  company  |user   |
#        |  company  |company|
#        |  user     |user   |
#        |  user     |company|


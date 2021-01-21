Feature:  check "Index" page media
#
#  Scenario Outline: check updating smartheat and top30 through endpoint
#      Given get endpoint image: <type>
#       And get endpoint image file
#       And get new image
#      When upload new image through endpoint: <type>
#       And get endpoint image: <type>
#      Then compare uploaded image with resulting image from endpoint
#       And upload original image through endpoint: <type>
#       Given check contests endpoint: <type>
#      Examples: cases
#     | type           |
#     | smartheat      |
#     | top30          |

#
#    Scenario Outline: check updating smartheat and top30 through riskbot
#      Given get endpoint image: <type>
#       And get endpoint image file
#       And get new image
#      When upload new image through Riskbot: <type>
#       And get endpoint image: <type>
#      Then compare uploaded image with resulting image from endpoint
#       And upload original image through Riskbot: <type>
#      Examples: cases
#     | type           |
#     | smartheat      |
#     | top30          |

#    Scenario Outline: check contest icons
#      Given get endpoint icon: <type>
#      Then compare actual icon with expected icon: <type>
#      Examples: cases
#     | type           |
#     | smartheat      |
#     | top30          |


      Scenario: check contest icons
      Given initiate news data
       And create news
       And get test_news id
      When perform likes process
       And perform likes process
       And perform views process
       And perform views process
      Then check all data of news
       And compare image of news with template image
        And pause - 10 sec(s)
       But delete created news
Feature:  check "Index" page

  Scenario Outline: check updating smartheat and top30 through endpoint
      Given get all books and sort by author
        And create url with random author
        And search of books
      Then check result of search
      Examples: cases
     | type           |
     | smartheat      |
     | top30          |
    | smartheat      |
     | top30          |
    | smartheat      |
     | top30          |
    | smartheat      |
     | top30          |
    | smartheat      |
     | top30          |
     | top30          |



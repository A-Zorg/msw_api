Feature:  check "Index" page
  @autorepeat @10
  Scenario: check library
      Given get all books and sort by author
        And create url with random author
        And search of books
      Then check result of search

  Scenario: check holidays
       Given get US holidays for this year
       Then compare holidays from endpoint

  Scenario: check /api/index/services_compensations/
       Given check /api/index/services_compensations/


  Scenario: CHECK /index/users/
       Given get users data from db
       Then compare data from endpoint and db

  Scenario: CHECK books categories
       Given get books categories from endpoint
       Then compare books_categories from endpoint and template

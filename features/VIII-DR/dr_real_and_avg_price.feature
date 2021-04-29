Feature: DR calculation real and avg_price

   @autorepeat @20
   Scenario: check calculation avg_price and real or premarket data
      Given get random ticker
       And from db get first DR_data_tuple: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==POS
       And from db get second DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==PRE
      Then [DR] check calculation: avg_price ans real in PropreportsData
#
   @autorepeat @20
   Scenario: check calculation avg_price and real or postmarket data
      Given get random ticker
       And from db get first DR_data_tuple: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==INT
       And from db get second DR_data_dictionary: request_name==propreportsdata_all, review_date==target_date, session==POS
      Then [DR] check calculation: avg_price ans real in PropreportsData

    @autorepeat @20
     Scenario: check calculation avg_price and real or intraday data
        Given get random ticker
         And from db get first DR_data_tuple: request_name==unrealizedpertickeraccount_not_0, review_date==target_date, session==PRE
         And from db get second DR_data_dictionary: request_name==propreportsdata_all, review_date==next_date, session==INT
        Then [DR] check calculation: avg_price ans real in PropreportsData

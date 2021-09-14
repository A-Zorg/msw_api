Feature: import from propreports_api

   Scenario: check import from propreports_api
      Given from propreports get data of selected SMRT046N for selected_data
#       And parse data from xls file
#       And clear review_propreportsdata db table for selected_data
#      When run propreports_api_daily_import for selected_data
#       And wait for task is finished: start_session_calculations
#       And from db get data of selected SMRT046N for selected_data
#      Then compare data from propreports and db
Feature: New Requests Controller

  Scenario: Upload new requests in CSV format
    Given the application is running
    When I access the "/upload-new-requests" endpoint
    And I attach a file named "valid_csv.csv"
    And I submit the form
    Then the rendered html should contain "Data inserted succesfully"

  Scenario: Upload new requests in Excel format
    Given the application is running
    When I access the "/upload-new-requests" endpoint
    And I attach a file named "sample_new_cases.xlsx"
    And I submit the form
    Then the rendered html should contain "Data inserted succesfully"
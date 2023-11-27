@update-password
Feature: Set Password
  Scenario: Update password for a new User
    Given the application is running
    When I access endpoint "/user/updatePassword?user=abcd-efgh" and enter a valid email "test3@tamu.edu"("Test User3"), password "abcd@1234567" and re-password "abcd@1234567"
    Then the Login Page should be displayed
  Scenario: Email or Password not present in POST request
    Given the application is running
    When I access the endpoint "/user/login" with JSON
    """
      {
        "name": "John Doe"
      }
      """
    Then the login response status code should be 400

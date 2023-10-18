Feature: Assign Requests Controller
  Scenario: Setup DB
    Given create db
  Scenario: View List of New Requests
    Given I am on the "new-requests" page
    When I view the list of new requests
    Then I should see a list of new requests with customer IDs, first names, and last names

  Scenario: Assign a New Request
    Given I am on the "new-requests" page
    When I click the "Assign" button for a new request
    And I select a user from the dropdown
    And I submit the assignment form
    Then I should see a success message

  Scenario: Purge DB
    Given: purge db
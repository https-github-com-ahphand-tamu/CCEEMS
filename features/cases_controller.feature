@cases-controller
Feature: Case Assignment
  Scenario: Assign case to a user
    Given there is a case with packet return status "RETURNED"
    And there is a user
    When the user assigns the case to the user
    Then the case should be assigned successfully

  Scenario: Try to assign a case with packet return status other than "RETURNED"
    Given there is a case with packet return status "WAITING"
    And there is a user
    When the user tries to assign the case to the user
    Then an error should be displayed indicating the case can't be assigned

  Scenario: Try to assign an invalid case or user
    Given there is an invalid case ID or user ID
    When the user tries to assign the case to the user
    Then an error should be displayed indicating an invalid case or user
@admin-controller
Feature: Admin Controller

  Scenario: Get a list of users
    Given the application is running
    When I access the "/admin/users" endpoint
    Then I should see user details

  Scenario: Get a user by ID
    Given the application is running
    When I access the "/admin/users/2" endpoint
    Then I should see that user's details

  Scenario: Add a new user
    Given the application is running
    When I send a POST request to "/admin/users" with JSON
      """
      {
        "name": "John Doe",
        "email": "johndoe@random.com",
        "role": "Admin"
      }
      """
    Then the response status code should be 201
    And the response should contain "User added successfully"

  Scenario: Update an existing user
    Given the application is running
    When I send a PUT request to "/admin/users/2" with JSON
      """
      {
        "name": "Updated John Doe",
        "email": "updatedjohndoe@example.com",
        "role": "Senior Leader"
      }
      """
    Then the response status code should be 200
    And the response should contain "User updated successfully"

  Scenario: Delete an user that does not exist
    Given the application is running
    When I send a DELETE request to "/admin/users/100"
    Then the response status code should be 404
    Then the response should contain "User not found"

  Scenario: Update password for a new User
    Given the application is running
    When I enter a valid password "abcd@1234567"
    Then the password should be updated in the database

  Scenario: User enters a password of invalid length
    Give the application is running
    When I enter an invalid password "abcd"
    Then I should see the message that password should be at least 8 characters long

  Scenario: User enters a passwords that do not match
    Given the application is running
    When I enter password "abcd#123456" and "abc#123456"
    Then I should see the message that both passwords should be the same.

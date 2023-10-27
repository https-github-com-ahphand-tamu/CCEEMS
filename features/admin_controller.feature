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

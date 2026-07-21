@Regression_Login
Feature: Login

  @skip_ci
  Scenario: Verify Login with invalid details
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user enters username
    And the user enters wrong password
    And the user clicks the eye icon in the password field
    And the user clicks Next
    Then the user should a message "Incorrect username or password."

  @skip_ci
  Scenario: Verify login with valid details
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user enters username
    And the user enters password
    And the user clicks the eye icon in the password field
    And the user clicks Next
    And the user enters OTP & clicks login
    Then the user should be directed to My Account

  Scenario: Verify login with empty password!
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user enters username
    And the user clicks Next
    Then the password field displays an inline message "Password is required"

  Scenario: Verify login with empty username!
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user enters password
    And the user clicks Next
    Then the username field displays an inline message "Username is required"

  Scenario: Verify login with empty username & password
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user clicks Next
    Then both the username field displays "Username is required" and the password field displays "Password is required"

  @skip_ci
  Scenario: Verify login with Invalid OTP
    Given the user visits the website "https://cib.sofriwebservices.com/"
    When the user enters username
    And the user enters password
    And the user clicks the eye icon in the password field
    And the user clicks Next
    And the user enters invalid OTP
    And the user clicks login
    Then the user sees "Invalid OTP. Please try again."
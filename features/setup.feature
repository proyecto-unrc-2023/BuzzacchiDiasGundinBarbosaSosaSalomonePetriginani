Feature: Setup

  Scenario: Start a new game
    Given the game is not started
    When we create a new game with an 50x50 board
    Then the game should be in spawn placement mode
    And the state of the board should be a 50x50 empty board

  Scenario: Grid Size Selection and Username Entry
    Given that I am on the game's homepage
    When I select the grid size "50x50"
    And I type the username "player1"
    And I click the "Start Game" button
    Then I should see the game's start screen

  Scenario: Team Selection
    Given that I am on the game start screen
    And I have already typed the username "player2"
    When I choose the team "Water Team"
    And I click the "Start Game" button
    Then I should see the game screen with the "Water Team"

  Scenario: Starting a Game with an Empty Username
    Given that I am on the game's homepage
    When I leave the username field empty
    And I select the grid size "75x75"
    And I click the "Start Game" button
    Then I should see an error message indicating that the username is required

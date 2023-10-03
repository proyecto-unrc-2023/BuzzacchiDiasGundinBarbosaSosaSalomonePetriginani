Feature: Spawns of cells

  Scenario: First spawn
    Given that the setup phase has been completed
    And the game is waiting
    When the user choose the position (3, 4) for the spawn and the spawn will create in the position (3, 4)
    Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION

#   Scenario: Second spawn
#     Given that we are playing the game
#     And the game is in the half game time
#     And the game shows on the screen to choose the position of the second spawn
#     When the user choose the position (3,10) for the spawn
#     Then the second spawn will create in the position (3,10)



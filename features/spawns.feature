Feature: Spawns of cells

  Scenario: First ice spawn
    Given that the setup phase has been completed
    And the game is waiting for put the ice spawn
    When the user choose the position (3, 4) for the ice spawn and the ice spawn will create in the position (3, 4)
    Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the ice spawn

  Scenario: First fire spawn
    Given that the setup phase has been completed
    And the game is waiting for put the fire spawn
    When the user choose the position (3, 4) for the fire spawn and the fire spawn will create in the position (3, 4)
    Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the fire spawn

#   Scenario: Second spawn
#     Given that we are playing the game
#     And the game is in the half game time
#     And the game shows on the screen to choose the position of the second spawn
#     When the user choose the position (3,10) for the spawn
#     Then the second spawn will create in the position (3,10)



 Feature: Spawns of cells

   Scenario: First ice spawn
     Given that the setup phase has been completed
     And the game is waiting for put the Ice spawn
     When the user choose the position (3, 4) for the Ice spawn and the Ice spawn will create in the position (3, 4)
     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Ice spawn

   Scenario: First fire spawn
     Given that the setup phase has been completed
     And the game is waiting for put the Fire spawn
     When the user choose the position (3, 4) for the Fire spawn and the Fire spawn will create in the position (3, 4)
     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Fire spawn

   Scenario: Second ice spawn
     Given that the user is playing the game for team Ice and has spawn at position (3, 4)
     And the game is in the half game time and the game shows on the screen to choose the position of the second Ice spawn
     When the user choose the position (3, 10) for the Ice spawn and the second Ice spawn will create in the position (3, 10)
     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION

   Scenario: Second fire spawn
     Given that the user is playing the game for team Fire and has spawn at position (3, 4)
     And the game is in the half game time and the game shows on the screen to choose the position of the second Fire spawn
     When the user choose the position (3, 10) for the Fire spawn and the second Fire spawn will create in the position (3, 10)
     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION


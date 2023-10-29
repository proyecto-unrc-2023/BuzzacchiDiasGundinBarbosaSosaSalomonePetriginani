#  Feature: Spawns of cells
#    Background: 
#     Given a new game is started in Spawn Placement mode
#     And a user with username Lucas is logged selecting team IceTeam
   
#   Scenario: First ice spawn   
#     Given the user choose the position (3, 4) for the Ice spawn 
#     When the Ice spawn creates in the position (3, 4)
#     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Ice spawn

#   Scenario: First fire spawn
#     Given the user choose the position (3, 4) for the Fire spawn 
#     When the Fire spawn creates in the position (3, 4)
#     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Fire spawn

  # Scenario: Creation of Cells
  #   Given the Ice spawn creates in the position (2,2)
  #   When the Spawn creates cells
  #   Then it should be create Ice cells in some adjacents positions of the spawn in (2, 2)

#   Scenario: Second ice spawn
#     Given that the user is playing the game for team Ice and has spawn at position (3, 4)
#     And the game is in the half game time and the game shows on the screen to choose the position of the second Ice spawn
#     When the user choose the position (3, 10) for the Ice spawn and the second Ice spawn will create in the position (3, 10)
#     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION
#
#   Scenario: Second fire spawn
#     Given that the user is playing the game for team Fire and has spawn at position (3, 4)
#     And the game is in the half game time and the game shows on the screen to choose the position of the second Fire spawn
#     When the user choose the position (3, 10) for the Fire spawn and the second Fire spawn will create in the position (3, 10)
#     Then the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION


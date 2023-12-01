Feature: Spawns of cells
  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Lucas is logged selecting team IceTeam
   
  Scenario: Generation of ice cells
    Given the user selects the position (1, 1) for the IceSpawn
    When the IceSpawn generate cells
    Then the cells must be created in one of the adjacents of the IceSpawn
    
  Scenario: Generation of fire cells
    Given the user selects the position (1, 1) for the FireSpawn
    When the FireSpawn generate cells
    Then the cells must be created in one of the adjacents of the FireSpawn
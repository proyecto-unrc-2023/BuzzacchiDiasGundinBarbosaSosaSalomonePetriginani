 Feature: Movement of cells from the same team
   Background: 
     Given a new game is started in Spawn Placement mode
     And a user with username Victoria is logged selecting team IceTeam
     And the user selects to put IceSpawn at the position (1,1)
     And simulation starts

   Scenario: Move level 1 Ice cell to an empty adjacent cell
     Given I have a level 1 IceCell at position (3, 3) with 15 health points
     And the adjacents cells at position of the IceCell (3, 3) are empty
     When I try to move the level 1 IceCell to an adjacent position
     Then the IceCell moves successfully to an adjacent position of (3, 3)
   
   Scenario: Move level 1 fire cell to an empty adjacent cell
     Given I have a level 1 FireCell at position (4, 4) with 16 health points
     And the adjacents cells at position of the FireCell (4, 4) are empty
     When I try to move the level 1 FireCell to an adjacent position
     Then the FireCell moves successfully to an adjacent position of (4, 4)
   
   Scenario: Move level 1 Ice cell to an empty adjacent cell
     Given I have a level 1 IceCell at position (13, 3) with 15 health points
     And the adjacents cells at position of the IceCell (3, 3) are empty
     When I try to move the level 1 IceCell to an adjacent position
     Then the IceCell moves successfully to an adjacent position of (3, 3)
   
   Scenario: Move level 1 fire cell to an empty adjacent cell
     Given I have a level 1 FireCell at position (10, 10) with 16 health points
     And the adjacents cells at position of the FireCell (10, 10) are empty
     When I try to move the level 1 FireCell to an adjacent position
     Then the FireCell moves successfully to an adjacent position of (4, 4)

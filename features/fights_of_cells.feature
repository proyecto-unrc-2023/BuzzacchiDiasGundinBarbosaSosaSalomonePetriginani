Feature: Fight of Cells

  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Genaro is logged selecting team IceTeam
    And the user selects to put IceSpawn at the position (20,20)
    And simulation starts

  Scenario: Two level 1 cells fight
    Given a level 1 IceCell with 8 life points at position (0,0)
    And a level 1 FireCell with 5 life points at position (0,0)
    When the fight starts
    Then the number of FireCells should be reduced by 1
    And the IceCell should win with 4 life points and level 1

  Scenario: Two level 3 cells fight
    Given a level 3 IceCell with 43 life points at position (1,1)
    And a level 3 FireCell with 41 life points at position (1,1)
    When the fight starts
    Then the number of FireCells should be reduced by 1
    And the IceCell should win with 39 life points and level 2

  Scenario: One level 1 IceCell against a level 2 FireCell
    Given a level 1 IceCell with 9 life points at position (2,2)
    And a level 2 FireCell with 22 life points at position (2,2)
    When the fight starts
    Then the number of IceCells should be reduced by 1
    And the FireCell should win with 18 life points and level 1

  Scenario: Multiple cells of different levels fight
    Given a level 2 IceCell with 25 life points at position (10,10)
    And a level 2 FireCell with 22 life points at position (10,10)
    And a level 1 IceCell with 12 life points at position (10,10)
    And a level 1 FireCell with 15 life points at position (10,10)
    When the fight starts
    Then the number of FireCells should be reduced by 2
    And the IceCell should win with 17 life points and level 1

  Scenario: A higher-level cell fights against lower-level cells
    Given a level 2 FireCell with 30 life points at position (0,0)
    And a level 1 IceCell with 15 life points at position (0,0)
    And a level 1 IceCell with 15 life points at position (0,0)
    When the fight starts
    Then the number of IceCells should be reduced by 2
    And the FireCell should win with 22 life points and level 2

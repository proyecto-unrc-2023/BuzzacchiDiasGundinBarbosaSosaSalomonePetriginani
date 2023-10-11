Feature: Fight of Cells

  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Genaro is logged selecting team IceTeam
    And same user selecs to put IceSpawn in (5,5)
    And simulation starts

  Scenario: Two level 1 cells fights
    Given there are two level 1 cells, one IceCell with 8 life points and one FireCell with 5 life points in position (0,0)
    When the fight starts
    Then the FireCell disappears from the battlefield and the IceCell wins with 4 life points and level 1

  Scenario: two level 3 cells fights
     Given there are two level 3 cells, one IceCell with 43 life points and one FireCell with 41 life points in position (1,1)
     When the fight starts
     Then the FireCell disappears from the battlefield and the IceCell wins with 39 life points and level 2

  Scenario: one level 1 IceCell against a level 2 FireCell
    Given there is one level 1 IceCell with 9 life points and one level 2 FireCell with 22 life points in position (2,2)
    When the fight starts
    Then the IceCell disappears from the battlefield and the FireCell wins with 18 life points and level 1

  #First battle starts, level 2 cells fight ends with IceCell winning with 21 life points and second battle starts, 
  # winning cell fights with level 1 FireCell, that finishes with a win for the same cell again
  Scenario: two fights, followed by an additional third one
    Given there are two level 2 cells, one IceCell with 25 life points and one FireCell with 22 life points in position (0,0)
    And there are two level 1 cells, one IceCell with 12 life points and one FireCell with 15 life points in position (0,0)
    When the fight starts
    Then we have two IceCells, level 1 cell with no fights, and the cells with 2 fights became level 1 with 17 life points

  Scenario: A higher-level cell fights against lower-level cells
    Given there is one FireCell with 30 life points at level 2 and two IceCells at level 1 with 15 life points each in position (0,0)
    When the fight starts
    Then the FireCell at level 2 wins, the IceCells disappear from the battlefield, and the FireCell wins with 22 life points

  # Este escenario necesita un metodo mas general que priorice la fusion por sobre la pelea
  # Scenario: two IceCell in same position with same level against a same one FireCell level
  #   Given there are two level 1 cells, one IceCell with 4 life points and one FireCell 9 life points in position (0,0)
  #   And there is a FireCell level 1 with 8 life points in the same position
  #   When the fight is going to start, then the fusion between IceCell cells starts first
  #   And a level 2 IceCell is created with 40 life points
  #   And level 2 IceCell fights against level one FireCell
  #   And level 2 IceCells wins with 36 life points and FireCell dies


 Feature: Movement of cells from the same team

   Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Victoria is logged selecting team IceTeam
    And same user selecs to put IceSpawn in (5,5)
    And simulation starts

  Scenario: Move level 1 ice cell to an empty adjacent cell
    Given I have a level 1 ice cell at position (3, 3) with 15 health points
    And the adjacent cell at position (4, 3) is empty
    When I try to move the level 1 ice cell to position (4, 3)
    Then the ice cell moves successfully to position (4, 3)

  Scenario: Move level 1 fire cell to an empty adjacent cell
    Given I have a level 1 fire cell at position (3, 3) with 16 health points
    And the adjacent cell at position (4, 3) is empty
    When I try to move the level 1 fire cell to position (4, 3)
    Then the fire cell moves successfully to position (4, 3)

#   Scenario: Attempt to move level 1 ice cell to a cell occupied by another level 1 cell
#     Given I have a level 1 ice cell with life 19 at position (3, 3)
#     And another level 1 ice cell whit life 15 at position (4, 3)
#     When I try to move the level 1 ice cell to position (4, 3)
#     Then the cells merge, generating a new level 2 cell at position (4, 3)

  Scenario: Attempt to move level 1 ice cell to an adjacent cell occupied by a level 3 cell
    Given I have a level 1 ice cell at position (3, 3) with 19 health points
    And I have a level 3 ice cell at position (4, 3) with 45 health points
    When I try to move the level 1 ice cell to position (4, 3)
    Then both cells cannot merge, and coexist at position (4, 3)

  Scenario: Attempt to move level 1 fire cell to an adjacent cell occupied by a level 3 cell
    Given I have a level 1 fire cell at position (3, 3) with 18 health points 
    And I have a level 3 fire cell at position (4, 3) with 41 health points
    When I try to move the level 1 fire cell to position (4, 3)
    Then both cells cannot merge, and coexist at position (4, 3)

  Scenario: Attempt to move level 2 ice cell to an adjacent cell occupied by a level 1 ice cell
    Given I have a level 2 ice cell at position (3, 3) with 26 health points
    And I have a level 1 ice cell at position (4, 3) with 9 health points
    When I try to move the level 2 ice cell to position (4, 3) with 26 health points
    Then both cells cannot merge, and coexist at position (4, 3)

  Scenario: Attempt to move level 2 fire cell to an adjacent cell occupied by a level 1 fire cell
    Given I have a level 2 fire cell at position (3, 3) with 30 health points
    And I have a level 1 fire cell at position (4, 3) with 2 health points
    When I try to move the level 2 fire cell to position (4, 3) with 30 health points
    Then both cells cannot merge, and coexist at position (4, 3)

#   Scenario: Move cell to a cell occupied by 2 cells of different levels same team (coexisting)
#     Given I have a level 1 fire cell at position (2, 2)
#     And a level 2 fire cell at position (2, 2)
#     And another level 1 fire cell at position (3, 2)
#     When I try to move the level 1 cell to position (2, 2)
#     Then the level 1 cells die, and the level 2 cell survives at position (2, 2)

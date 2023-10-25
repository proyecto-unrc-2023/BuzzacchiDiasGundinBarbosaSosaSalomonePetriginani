Feature: Movement of cells from the same team

  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Victoria is logged selecting team IceTeam
    And the user selects to put Ice Spawn at the position (1,1)
    And simulation starts

  Scenario: Move level 1 Ice cell to an empty adjacent cell
    Given I have a level 1 Ice cell at position (3, 3) with 15 health points
    And the adjacents cells at position of the Ice cell (3, 3) are empty
    When I try to move the level 1 Ice cell to an adjacent position
    Then the Ice cell moves successfully to an adjacent position of (3, 3)

  Scenario: Move level 1 fire cell to an empty adjacent cell
    Given I have a level 1 Fire cell at position (4, 4) with 16 health points
    And the adjacents cells at position of the Fire cell (4, 4) are empty
    When I try to move the level 1 Fire cell to an adjacent position
    Then the Fire cell moves successfully to an adjacent position of (4, 4)

  Scenario: Move level 1 Ice cell to an empty adjacent cell
    Given I have a level 1 Ice cell at position (13, 3) with 15 health points
    And the adjacents cells at position of the Ice cell (3, 3) are empty
    When I try to move the level 1 Ice cell to an adjacent position
    Then the Ice cell moves successfully to an adjacent position of (3, 3)

  Scenario: Move level 1 fire cell to an empty adjacent cell
    Given I have a level 1 Fire cell at position (10, 10) with 16 health points
    And the adjacents cells at position of the Fire cell (10, 10) are empty
    When I try to move the level 1 Fire cell to an adjacent position
    Then the Fire cell moves successfully to an adjacent position of (4, 4)

# #   Scenario: Attempt to move level 1 ice cell to a cell occupied by another level 1 cell
# #     Given I have a level 1 ice cell with life 19 at position (3, 3)
# #     And another level 1 ice cell whit life 15 at position (4, 3)
# #     When I try to move the level 1 ice cell to position (4, 3)
# #     Then the cells merge, generating a new level 2 cell at position (4, 3)

#  Scenario: Attempt to move level 1 ice cell to an adjacent cell occupied by a level 3 cell
#    Given I have a level 1 Ice cell at position (3, 3) with 19 health points
#    And  there are level 3 Ice cells at adjacents positions of (3, 3) with 60 health points
#    When I try to move the Ice cells to an adjacent position
#    Then the cells cannot merge, and coexist in the board
#
#  Scenario: Attempt to move level 1 fire cell to an adjacent cell occupied by a level 3 cell
#    Given I have a level 1 Fire cell at position (5, 5) with 18 health points 
#    And there are level 3 Fire cells at adjacents positions of (4, 3) with 55 health points
#    When I try to move the Fire cells to an adjacent position
#    Then the cells cannot merge, and coexist in the board
#
#  Scenario: Attempt to move level 2 ice cell to an adjacent cell occupied by a level 1 ice cell
#    Given I have a level 2 Ice cell at position (6, 6) with 26 health points
#    And there are level 1 Ice cells at adjacents positions of (6, 6) with 9 health points
#    When I try to move the Ice cells to an adjacent position
#    Then the cells cannot merge, and coexist in the board
#
#  Scenario: Attempt to move level 2 fire cell to an adjacent cell occupied by a level 1 fire cell
#    Given I have a level 2 Fire cell at position (7, 7) with 30 health points
#    And there are level 1 Fire cells at adjacents positions of (7, 7) with 2 health points
#    When I try to move the Fire cells to an adjacent position
#    Then the cells cannot merge, and coexist in the board
#
## #   Scenario: Move cell to a cell occupied by 2 cells of different levels same team (coexisting)
## #     Given I have a level 1 fire cell at position (2, 2)
## #     And a level 2 fire cell at position (2, 2)
## #     And another level 1 fire cell at position (3, 2)
## #     When I try to move the level 1 cell to position (2, 2)
## #     Then the level 1 cells die, and the level 2 cell survives at position (2, 2)
#
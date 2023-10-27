  Feature: Fusion of Cells

  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Fernando is logged selecting team IceTeam
    And the user selects to put Ice Spawn at the position (5,5)
    And simulation starts


  Scenario: Fusion Two Level 1 Ice Cells
    Given a level 1 Ice cell at position (3, 3) with 5 health points
    And a level 1 Ice cell at position (3, 3) with 10 health points
    When fusion start at position (3, 3)
    Then a level 2 Ice cell is created at position (3, 3) with 40 health points and the level 1 Ice cells at (3, 3) disappears from the battlefield

  Scenario: Fusion Two Level 2 Fire Cells
    Given a level 2 Fire cell at position (8, 8) with 37 health points
    And a level 2 Fire cell at position (8, 8) with 28 health points
    When fusion start at position (8, 8)
    Then a level 3 Fire cell is created at position (8, 8) with 60 health points and the level 2 Fire cells at (8, 8) disappears from the battlefield

  Scenario: Attempt to merge two level 3 Ice cells
    Given a level 3 Ice cell at position (9, 9) with 53 health points
    And a level 3 Ice cell at position (9, 9) with 45 health points
    When fusion start at position (9, 9)
    Then the Ice cells cannot merge, and both coexist two cells level 3 with 53 health points and other cell level 3 with 45 health points at position (9, 9)

  Scenario: Attempt to merge a level 2 Fire cell with a level 3 Fire cell
    Given a level 2 Fire cell at position (3, 3) with 30 health points
    And a level 3 Fire cell at position (3, 3) with 50 health points
    When fusion start at position (3, 3)
    Then the Fire cells cannot merge, and both coexist two cells level 2 with 30 health points and other cell level 3 with 50 health points at position (3, 3)

   Scenario: Attempt to merge three level 1 Ice cells
     Given a level 1 Ice cell at position (20, 10) with 6 health points
     And a level 1 Ice cell at position (20, 10) with 15 health points
     And a level 1 Ice cell at position (20, 10) with 19 health points
     When fusion start at position (20, 10)
     Then a level 2 Ice cell is created at position (20, 10) with 40 health points and only one level 1 Ice cell at (20, 10) with 6 health points disappears from the battlefield

  Scenario: Merge four level 1 Fire cells into two level 3 cells
    Given a level 1 Fire cell at position (8, 2) with 12 health points
    And a level 1 Fire cell at position (8, 2) with 1 health points
    And a level 1 Fire cell at position (8, 2) with 17 health points
    And a level 1 Fire cell at position (8, 2) with 20 health points
    When fusion start at position (8, 2)
    Then a level 3 Fire cells is created at position (8, 2) with 60 health points and all level 1 Fire cells at (8, 2) disappears from the battlefield

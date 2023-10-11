 Feature: Fusion of Cells

  Background: 
    Given a new game is started in Spawn Placement mode
    And a user with username Victoria is logged selecting team IceTeam
    And same user selecs to put IceSpawn in (5,5)
    And simulation starts

  Scenario: Fusion Two Level 1 Ice Cells
      Given I have a level 1 ice cell at position (3, 3) with 5 health points
      And I have a level 1 ice cell at position (3, 3) with 10 health points
      When fusion start at position (3, 3)
      Then a level 2 ice cell is created at position (3, 3) with 40 health points and the level 1 ice cells at (3, 3) disappears from the battlefield

  Scenario: Fusion Two Level 2 Fire Cells
    Given I have a level 2 fire cell at position (4, 4) with 37 health points
    And I have a level 2 fire cell at position (4, 4) with 28 health points
    When fusion start at position (4, 4)
    Then a level 3 fire cell is created at position (4, 4) with 60 health points and the level 2 fire cells at (4, 4) disappears from the battlefield

  Scenario: Attempt to merge two level 3 ice cells
    Given I have a level 3 ice cell at position (5, 5) with 53 health points
    And I have a level 3 ice cell at position (5, 5) whit 45 health points
    When fusion start at position (5, 5)
    Then the cells cannot merge, and both coexist two cells level 3 with 53 health points and other cell level 3 with 45 health points at position (5, 5)

  Scenario: Attempt to merge a level 2 fire cell with a level 3 fire cell
    Given I have a level 2 fire cell at position (3, 3) with 30 health points
    And I have a level 3 fire cell at position (3, 3) with 50 health points
    When fusion start at position (3, 3)
    Then the cells cannot merge, and both coexist two cells level 2 with 30 health points and other cell level 3 with 50 health points at position (3, 3)

   Scenario: Attempt to merge three level 1 ice cells
     Given I have a level 1 ice cell at position (6, 5) with 6 health points
     And I hace a level 1 ice cell at position (6, 5) with 15 health points
     And I have level 1 ice cell at position (6, 5) with 19 health points
     When fusion start at position (6, 5)
     Then a level 2 ice cell is created at position (6, 5) with 40 health points and only one level 1 ice cell at (6, 5) with 19 health points disappears from the battlefield

  Scenario: Merge four level 1 fire cells into two level 3 cells
    Given I have a level 1 fire cell at position (8,2) with 12 health points
    And I have a level 1 fire cell at position (8, 2) with 1 health points
    And I have a level 1 fire cell at position (8, 2) with 17 health points
    And I have a level 1 fire cell at position (8, 2) with 20 health points
    When fusion start at position (8, 2)
    Then a level 3 fire cells is created at position (8, 2) with 60 health points and all level 1 fire cells at (8, 2) disappears from the battlefield

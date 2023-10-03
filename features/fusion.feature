 Feature: Fusion of Cells

    Scenario: Fusion Two Level 1 Ice Cells
        Given I have a level 1 ice cell at position (3, 3) with 5 health points
        And another level 1 ice cell at position (3, 3) with 10 health points
        When fusion start at position (3,3)
        Then a level 2 ice cell is created at position (3, 3) with 40 health points and the level 1 ice cells at (3, 3) disappears from the battlefield

  Scenario: Fusion Two Level 2 Fire Cells
    Given I have a level 2 fire cell at position (4, 4) with 37 health points
    And another level 2 fire cell at position (4, 4) with 28 health points
    When fusion start at position (4,4)
    Then a level 3 fire cell is created at position (4, 4) with 60 health points and the level 2 fire cells at (4, 4) disappears from the battlefield

  Scenario: Attempt to merge two level 3 ice cells
    Given I have a level 3 ice cell at position (5, 5)
    And another level 3 ice cell at position (5, 5)
    When fusion start at position (5,5)
    Then the cells cannot merge, and both coexist at position (5, 5)

  Scenario: Attempt to merge a level 2 fire cell with a level 3 fire cell
    Given I have a level 2 fire cell at position (3, 3)
    And a level 3 fire cell at position (3, 3)
    When fusion start at position (3,3)
    Then the cells cannot merge and both coexist in (3,3)

#   Scenario: Attempt to merge three level 1 cells
#     Given I have a level 1 cell at position (3, 3)
#     And another level 1 cell at position (3, 4)
#     And a third level 1 cell at position (3, 5)
#     When I move the cell at (3, 3) to (3, 4)
#     And I attempt to move the remaining cell at (3, 5) to (3, 4)
#     Then the two cells with the highest life points merge, creating a new level 2 cell
#     And the new level 2 cell coexists with the other level 1 cell

#   Scenario: Merge four level 1 cells into two level 2 cells
#     Given I have a level 1 cell at position (3, 3)
#     And another level 1 cell at position (3, 4)
#     And a third level 1 cell at position (3, 5)
#     And a fourth level 1 cell at position (2,4)
#     When I move the cell at (3, 3) to (3, 4)
#     And I move the cell at (3, 5) to (3, 4)
#     And I move the cell at (2,4) to (3, 4)
#     Then two new level 2 cells coexist in the same cell at position (3, 4)

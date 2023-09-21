# Feature: Fusion of Cells

#   Scenario: Merge two level 1 cells
#     Given I have a level 1 cell at position (3, 3)
#     And another level 1 cell at position (3, 4)
#     When I move the cell at (3, 3) to (3, 4)
#     Then a level 2 cell is created at position (3, 4) with 20 health points
#     And the cell at (3, 3) disappears from the battlefield

#   Scenario: Merge two level 2 cells
#     Given I have a level 2 cell at position (4, 4)
#     And another level 2 cell at position (4, 5)
#     When I move the cell at (4, 4) to (4, 5)
#     Then a level 3 cell is created at position (4, 5) with 30 health points
#     And the cell at (4, 4) disappears from the battlefield

#   Scenario: Attempt to merge two level 3 cells
#     Given I have a level 3 cell at position (5, 5)
#     And another level 3 cell at position (5, 6)
#     When I move the cell at (5, 5) to (5, 6)
#     Then the cells cannot merge, and both coexist at position (5, 6)

#   Scenario: Attempt to merge a level 2 cell with a level 3 cell of the same team
#     Given I have a level 2 cell at position (3, 3)
#     And a level 3 cell at position (3, 4)
#     When I attempt to move the cell at (3, 3) to (3, 4)
#     Then the cells cannot merge and both coexist in (3,4)

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

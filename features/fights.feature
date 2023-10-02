Feature: Fight of Cells

   Scenario: Two level 1 cells fights
     Given there are two cells, one IceCell with 8 life points and one FireCell with 5 life points level 1 in position (0,0)
     When the fight starts
     Then the FireCell disappears from the battlefield

#   Scenario: Two level 3 cells fights
#     Given i have two cells of the same level
#     And one of them has more life points than the other
#     And the cell with more life points is in the position (4,4)
#     And the other cell in the position (4,6)
#     When the cell with more life points moves to the position (4,5)
#     And the other cell moves to the position (4,5)
#     Then the cell with less life points disappears from the battlefield
#     And the winning cell drops to level 2

#   Scenario: fight a level 1 against a level 2
#     Given i have two cells, one with level 1 and the other with level 2
#     And the cell with level 2 is in the position (4,4)
#     And the other cell is in the position (4,6)
#     When both cells move to the position (4,5)
#     Then the cell with less level disappears from the battlefield
#     And the winning cell drops to level 1

#   Scenario: fight a level 1 against a level 3
#     Given i have two cells, one with level 1 and the other with level 3
#     And the cell with level 3 is in the position (4,4)
#     And the other cell is in the position (4,6)
#     When both cells move to the position (4,5)
#     Then the cell with less level disappears from the battlefield
#     And the winning cell drops to level 2

#   Scenario: two fights in the same position
#     Given there are two level 2 cells in position (0,0), one FireCell with 22 life points and one IceCell with 25 life points
#     And there are two cells level 1 in position (0,0), one IceCell with 12 life points and one FireCell with 15 life points
#     When the cells with same level start the fight
#     Then level 1 FireCell dies and IceCell level 1 wins now with 24 life points
#     And level 2 FireCell wins fight with 14 life points now and level 2 IceCell dies 

#   Scenario: two IceCell in same position with same level against a same one FireCell level
#     Given there are two level 1 cells in position (0,0), one with 4 life points and the other with 9 life points
#     And there is a FireCell level 1 with 8 life points in the same position
#     When the fight is going to start
#     Then the fusion between IceCell cells starts first
#     And a level 2 IceCell is created with 20 life points
#     And level 2 IceCell fights against level one FireCell
#     And level 2 IceCells wins with 19 life points and FireCell dies
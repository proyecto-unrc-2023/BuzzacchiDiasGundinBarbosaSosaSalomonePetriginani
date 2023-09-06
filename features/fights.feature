Feature: Fight of Cells

  Scenario: Two level 1 cells fights
    Given i have two cells of the same level
    And one of them has more life points than the other
    And the cell with more life points is in the position (4,4)
    And the other cell in the position (4,6)
    When the cell with more life points moves to the position (4,5)
    And the other cell moves to the position (4,5)
    Then the cell with less life points disappears from the battlefield

  Scenario: Two level 2 cells fights
    Given i have two cells of the same level
    And one of them has more life points than the other
    And the cell with more life points is in the position (9,4)
    And the other cell in the position (9,6)
    When the cell with more life points moves to the position (9,5)
    And the other cell moves to the position (9,5)
    Then the cell with less life points disappears from the battlefield
    And the winning cell drops to level 1

  Scenario: Two level 3 cells fights
    Given i have two cells of the same level
    And one of them has more life points than the other
    And the cell with more life points is in the position (4,4)
    And the other cell in the position (4,6)
    When the cell with more life points moves to the position (4,5)
    And the other cell moves to the position (4,5)
    Then the cell with less life points disappears from the battlefield
    And the winning cell drops to level 2

  Scenario: fight a level 1 against a level 2
    Given i have two cells, one with level 1 and the other with level 2
    And the cell with level 2 is in the position (4,4)
    And the other cell is in the position (4,6)
    When both cells move to the position (4,5)
    Then the cell with less level disappears from the battlefield
    And the winning cell drops to level 1

  Scenario: fight a level 2 against a level 3
    Given i have two cells, one with level 2 and the other with level 3
    And the cell with level 3 is in the position (4,4)
    And the other cell is in the position (4,6)
    When both cells move to the position (4,5)
    Then the cell with less level disappears from the battlefield
    And the winning cell drops to level 2

  Scenario: fight a level 1 against a level 3
    Given i have two cells, one with level 1 and the other with level 3
    And the cell with level 3 is in the position (4,4)
    And the other cell is in the position (4,6)
    When both cells move to the position (4,5)
    Then the cell with less level disappears from the battlefield
    And the winning cell drops to level 2

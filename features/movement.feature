Feature: Movement of cells from the same team

  Scenario: Move level 1 cell to an empty adjacent cell
    Given I have a level 1 cell at position (3, 3)
    And the adjacent cell at position (4, 3) is empty
    When I try to move the cell to position (4, 3)
    Then the cell moves successfully to position (4, 3)

  Scenario: Attempt to move level 1 cell to a cell occupied by another level 1 cell
    Given I have a level 1 cell at position (3, 3)
    And another level 1 cell at position (4, 3)
    When I try to move the cell to position (4, 3)
    Then the cells merge, generating a new level 2 cell at position (4, 3)

  Scenario: Attempt to move level 1 cell to an adjacent cell occupied by a level 3 cell
    Given I have a level 1 cell at position (3, 3)
    And a level 3 cell at position (4, 3)
    When I try to move the level 1 cell to position (4, 3)
    Then both cells coexist in cell (4, 3)

  Scenario: Attempt to move level 2 cell to an adjacent cell occupied by a level 1 cell
    Given I have a level 2 cell at position (3, 3)
    And a level 1 cell at position (4, 3)
    When I try to move the level 2 cell to position (4, 3)
    Then the cells cannot merge, and both coexist at position (4, 3)

  Scenario: Move cell to a cell occupied by 2 cells of different levels (coexisting)
    Given I have a level 1 cell at position (2, 2)
    And a level 2 cell at position (2, 2)
    And another level 1 cell at position (3, 2)
    When I try to move the level 1 cell to position (2, 2)
    Then the level 1 cells die, and the level 2 cell survives at position (2, 2)

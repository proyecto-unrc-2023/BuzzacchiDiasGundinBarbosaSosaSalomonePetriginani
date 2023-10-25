Feature: Fight of Spawns

    Background:
        Given a new game is started in Spawn Placement mode
        And a user with username Genaro is logged selecting team IceTeam
        And the user selects to put Ice Spawn at the position (1,1)
        And simulation starts

    Scenario: One level 1 fire cell fight vs ice spawn
        Given a level 1 Fire Cell with 16 life points at position (0,1)
        When the fight starts
        Then the ice spawn has 284 life points and the cell(s) dies

    Scenario: 3 level 2 fire cell fight vs ice spawn
        Given a level 2 Fire Cell with 33 life points at position (2,1)
        And a level 2 Fire Cell with 40 life points at position (2,0)
        And a level 2 Fire Cell with 25 life points at position (0,2)
        When the fight starts
        Then the ice spawn has 202 life points and the cell(s) dies

    Scenario: Defeat of the Spawn
        Given the Ice Spawn has 35 life points
        And a level 2 Fire Cell with 38 life points at position (2,2)
        When the fight starts
        Then the ice spawn dies and the game ends
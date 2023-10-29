Feature: Fight of Spawns

    Background:
        Given a new game is started in Spawn Placement mode
        And a user with username Genaro is logged selecting team IceTeam
        And the user selects to put IceSpawn at the position (1,1)
        And simulation starts

    Scenario: One level 1 fire cell fight vs ice spawn
        Given a level 1 FireCell with 16 life points at position (0,1)
        When the fight starts
        Then the IceSpawn has 284 life points and the cell(s) dies

    Scenario: 3 level 2 firecell fight vs ice spawn
        Given a level 2 FireCell with 33 life points at position (2,1)
        And a level 2 FireCell with 40 life points at position (2,0)
        And a level 2 FireCell with 25 life points at position (0,2)
        When the fight starts
        Then the IceSpawn has 202 life points and the cell(s) dies

    Scenario: Defeat of the Spawn
        Given the IceSpawn has 35 life points
        And a level 2 FireCell with 38 life points at position (2,2)
        When the fight starts
        Then the IceSpawn dies and the game ends
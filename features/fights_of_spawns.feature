Feature: Fight of Spawns

    Background:
        Given a new game is started in Spawn Placement mode
        And a user with username Genaro is logged selecting team IceTeam
        And the user selects to put Ice Spawn at the position (1,1)
        And simulation starts

    Scenario: One level 1 fire cell fight vs ice spawn
        Given a level 1 Fire Cell with 16 life points at position (0,1)
        When the fight starts
        Then the ice spawn loses 16 life points and is left with 284 life points

    
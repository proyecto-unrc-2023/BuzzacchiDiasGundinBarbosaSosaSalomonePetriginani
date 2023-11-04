#  Feature: Healing Area

#     Background: 
#      Given a new game is started in Spawn Placement mode
#      And a user with username Victoria is logged selecting team IceTeam
#      And the user selects to put IceSpawn at the position (5,5)
#      And simulation starts

#    Scenario: Level 1 IceCell in Healing Area
#      Given there is a level 1 IceCell with 15 life points in position (1,1)
#      And a HealingArea affecting IceCell is at position (1,1) and its adjacent
#      When the IceCell HealingArea effect is applied
#      Then the IceCell at position (1,1) should have 18 life points

#   Scenario: Level 1 IceCell ready to level up in Healing Area
#     Given there is a level 1 IceCell with 19 life points in position (1,1)
#     And a HealingArea affecting IceCell is at position (1,1) and its adjacent
#     When the IceCell HealingArea effect is applied
#     Then the IceCell at position (1,1) should have 22 life points and should level up to level 2
#
#   Scenario: Level 3 IceCell in Healing Area
#     Given there is a level 3 IceCell with 60 life points in position (1,1)
#     And a HealingArea affecting IceCell is at position (1,1) and its adjacent
#     When the IceCell HealingArea effect is applied
#     Then the IceCell at position (1,1) should remain at level 3 with 60 life points
#
#    Scenario: Level 1 FireCell in IceCell Healing Area
#     Given there is a Level 1 FireCell with 17 life points at position (1,1)
#     And an IceCell Healing Area is at position (1,1) and its adjacent
#     When the IceCell Healing Area effect is applied
#     Then the FireCell at position (1,1) should have 17 life points
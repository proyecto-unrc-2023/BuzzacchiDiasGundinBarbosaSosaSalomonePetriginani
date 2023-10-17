# Feature: Healing Area

#   Scenario: Level 1 IceCell in Healing Area
#     Given there is a level 1 IceCell with 15 life points in position (1,1)
#     And a HealingArea affecting IceCells is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
#     When the HealingArea effect is applied
#     Then the IceCell at position (1,1) should have 18 life points

#   Scenario: Level 1 IceCell ready to level up in Healing Area
#     Given there is a level 1 IceCell with 19 life points in position (1,1)
#     And a HealingArea IceCells is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
#     When healing area applies effect
#     Then the IceCell at position (1,1) should have 22 life points
#     And the IceCell should level up to level 2

#   Scenario: Level 3 IceCell in Healing Area
#     Given there is a level 3 IceCell with 60 life points in position (1,1)
#     And an Ice healing area is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
#     When the HealingArea heals
#     Then the IceCell at position (1,1) should remain at level 3 with 60 life points

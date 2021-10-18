"""
Advance wars uses a damage table for the base damage of each unit-unit matchup
This will let units use a method to attack that gives their own code and the enemy unit's code,
i.e.
cursor.selection.attack(blocking_entity)
    damage = damage_table[self.code][enemy.code]
"""

"""

"""


table = dict(
    inf={"inf": 55, "mec": 55},
    mec={"inf": 55, "mec": 55}
)

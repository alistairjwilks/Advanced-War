import numpy as np


class Power:
    pass


class CO:
    def __init__(
            self, name: str,
            damage_mod: dict = {},
            defence_mod: dict = {},
            power: Power = None,
            super_power: Power = None,
            luck_min: int = 0,
            luck_max: int = 9
    ):
        self.luck_max = luck_max
        self.luck_min = luck_min
        self.super_power = super_power
        self.power = power
        self.defence_mod = defence_mod
        self.damage_mod = damage_mod
        self.name = name

    def luck_roll(self) -> int:
        if self.luck_min >= 0:
            return np.random.randint(self.luck_min, self.luck_max + 1)
        else:
            return np.random.randint(self.luck_min, 1) + np.random.randint(0, self.luck_max + 1)

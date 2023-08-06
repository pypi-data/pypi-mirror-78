import itertools
from Fortuna import distribution_range, middle_linear, plus_or_minus_linear
from MonsterGen.monster_lib import monster_stats, CR, random_monster_type
from MonsterGen.monster_manual import random_monster_by_type


__all__ = ("Monster", )


class Monster:

    def __init__(self, cr, monster_type=None, name=None):
        self.monster_type = monster_type if monster_type else random_monster_type()
        self.cr = CR(cr) if type(cr) == int else cr
        self.name = name if name else random_monster_by_type(self.monster_type)
        self.variance = plus_or_minus_linear(3)
        self.hp_range = monster_stats["HP Range"][self.cr.key]
        self.hp = distribution_range(middle_linear, *self.hp_range)
        self.ac = monster_stats["AC"][self.cr.key] + self.variance
        self.att = monster_stats["ATT"][self.cr.key] - self.variance
        self.dc = monster_stats["DC"][self.cr.key]
        self.damage_range = monster_stats["Damage Range"][self.cr.key]
        self.damage = distribution_range(middle_linear, *self.damage_range)
        self.xp = monster_stats["XP"][self.cr.key]

    def to_dict(self):
        lo_dam, hi_dam = self.damage_range
        damage = f"{lo_dam} - {hi_dam}"
        return {
            "Name": self.name,
            "Type": self.monster_type,
            "CR": self.cr.string,
            "Hit Points": self.hp,
            "Armor Class": self.ac,
            "Attack Bonus": self.att,
            "Typical Damage": damage,
            "Save DC": self.dc,
            "XP Value": self.xp,
        }

    def __str__(self):
        output = (f"{k}: {v}" for k, v in self.to_dict().items())
        return '\n'.join(itertools.chain(output, ('',)))


if __name__ == '__main__':
    print()
    monster_cr = CR.party_adapter(average_level=3, num_players=6, difficulty=3)
    print(Monster(monster_cr))
    print(Monster(monster_cr))

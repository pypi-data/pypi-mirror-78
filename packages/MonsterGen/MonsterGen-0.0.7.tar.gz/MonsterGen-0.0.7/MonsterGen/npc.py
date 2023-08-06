import itertools
from Fortuna import plus_or_minus_gauss, d
from MonsterGen.npc_lib import random_background, random_profession
from MonsterGen.npc_lib import random_appearance, random_mannerism, random_race


__all__ = ("Npc", )


class Npc:

    def __init__(self):
        self.name = "NPC"
        self.profession = random_profession()
        self.race = random_race()
        self.appearance = random_appearance()
        self.mannerism = random_mannerism()
        self.background = random_background()
        self.health = 9 + plus_or_minus_gauss(3)
        self.ac = 9 + plus_or_minus_gauss(3)
        self.damage = d(4)

    def to_dict(self):
        return {
            "Profession": self.profession,
            "Race": self.race,
            "Background": self.background,
            "Appearance": self.appearance,
            "Mannerism": self.mannerism,
            "Hit Points": self.health,
            "Armor Class": self.ac,
            "Damage": self.damage,
        }

    def __str__(self):
        output = "\n".join(itertools.chain(
            (f"{k}: {v}" for k, v in self.to_dict().items()), ('',))
        )
        return output


if __name__ == "__main__":
    for _ in range(10):
        print(Npc())

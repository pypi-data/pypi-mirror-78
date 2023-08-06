import itertools
from Fortuna import TruffleShuffle, FlexCat
from MonsterGen.monster_lib import CR


__all__ = ("random_trap", )


class Trap:
    type = "Trap"
    spot_dc = 10
    save_dc = 11
    rank_0_damage = "1d2"
    rank_1_damage = "2d4"
    rank_2_damage = "3d6"
    rank_3_damage = "4d8"
    rank_4_damage = "5d10"
    random_ability = TruffleShuffle(("CON", "STR", "DEX", "INT", "WIS"))
    random_trap = FlexCat({
        'bludgeoning': (
            "Falling Rocks", "Swinging Hammer", "Falling Chandelier",
        ),
        'falling': (
            "Deep Pit", "Spring Loaded Floor Tile", "Greased Slide",
            "False Floor",
        ),
        'piercing': (
            "Spiked Pit", "Guided Arrow", "Flying Broken Glass",
            "Falling Chandelier of Spikes",
        ),
        'slashing': (
            "Swinging Blade", "Guillotine", "Hooks and Chains",
            "Cloud of Daggers", "Exploding Mirror",
        ),
        'poison': (
            "Poison Dart", "Noxious Gas", "Pit Vipers", "Exploding Rotten Corpse",
        ),
        'acid': (
            "Acid Spay", "Acid Pool", "Acidic Bile", "Dripping Acidic Goo",
        ),
        'fire': (
            "Flame Jet", "Explosive Gas", "Lava Pit", "Delayed Fireball Blast",
            "Inferno",
        ),
        'lightning': (
            "Lightning Rod", "Tesla Coil", "Electric Trip Wire", "Lightning Bolt",
        ),
        'cold': (
            "Frozen Ground", "Cone of Cold", "Hail Storm", "Freeze the Flesh",
            "Ice Lance",
        ),
        'necrotic': (
            "Putrid Spores", "Cloud of Decay", "Energy Drain", "Beam of Entropy",
        ),
    }, key_bias="truffle_shuffle", val_bias="truffle_shuffle")

    def __init__(self, cr, dam_type=None):
        self.cr = CR(cr)
        self.save_vs = self.random_ability()
        self.xp = self.set_xp_by_cr(self.cr)
        if dam_type:
            self.damage_type = dam_type
        else:
            self.damage_type = self.random_trap.random_cat()
        self.name = self.random_trap(self.damage_type)
        self.damage = self.set_damage(self.cr)

    def set_damage(self, cr):
        if cr.val < 1:
            damage = self.rank_0_damage
        elif cr.val < 5:
            damage = self.rank_1_damage
        elif cr.val < 11:
            damage = self.rank_2_damage
        elif cr.val < 17:
            damage = self.rank_3_damage
        else:
            damage = self.rank_4_damage
        return damage

    @staticmethod
    def set_xp_by_cr(cr):
        xp_lookup = (
            10, 25, 50, 100,
            200, 450, 700, 1100, 1800,
            2300, 2900, 3900, 5000, 5900,
            7200, 8400, 10000, 11500, 13000,
            15000, 18000, 20000, 22000, 25000,
            33000, 41000, 50000, 62000, 155000,
            155000, 155000, 155000, 155000, 155000,
            155000, 155000, 155000, 155000, 155000,
        )
        return xp_lookup[cr.key]

    def __lt__(self, other):
        return self.cr <= other.cr

    def to_dict(self):
        return {
            "Name": self.name,
            "Type": self.type,
            "CR": self.cr.string,
            "Spot & Disarm DC": self.spot_dc,
            "Save vs": f"{self.save_vs} DC {self.save_dc} for half damage",
            "Damage": f"{self.damage} {self.damage_type}",
            "Disarm XP": self.xp,
        }

    def __str__(self):
        output = "\n".join(itertools.chain(
            (f"{k}: {v}" for k, v in self.to_dict().items()), ('',))
        )
        return output


class MinorTrap(Trap):
    type = "Minor Trap"
    spot_dc = 10
    save_dc = 11
    rank_0_damage = "1d4"
    rank_1_damage = "2d4"
    rank_2_damage = "3d4"
    rank_3_damage = "4d4"
    rank_4_damage = "5d4"


class DangerousTrap(Trap):
    type = "Dangerous Trap"
    spot_dc = 12
    save_dc = 15
    rank_0_damage = "1d6"
    rank_1_damage = "2d6"
    rank_2_damage = "3d6"
    rank_3_damage = "4d6"
    rank_4_damage = "5d6"


class DeadlyTrap(Trap):
    type = "Deadly Trap"
    spot_dc = 16
    save_dc = 20
    rank_0_damage = "1d8"
    rank_1_damage = "2d8"
    rank_2_damage = "3d8"
    rank_3_damage = "4d8"
    rank_4_damage = "5d8"


class EpicTrap(Trap):
    type = "Epic Trap"
    spot_dc = 18
    save_dc = 22
    rank_0_damage = "1d10"
    rank_1_damage = "2d10"
    rank_2_damage = "3d10"
    rank_3_damage = "4d10"
    rank_4_damage = "5d10"


class LegendaryTrap(Trap):
    type = "Legendary Trap"
    spot_dc = 20
    save_dc = 24
    rank_0_damage = "1d12"
    rank_1_damage = "2d12"
    rank_2_damage = "3d12"
    rank_3_damage = "4d12"
    rank_4_damage = "5d12"


random_trap_by_tier = FlexCat({
    "0": (MinorTrap, ),
    "1": (MinorTrap, DangerousTrap, DeadlyTrap),
    "2": (DangerousTrap, MinorTrap, DeadlyTrap, EpicTrap),
    "3": (DeadlyTrap, DangerousTrap, EpicTrap, MinorTrap),
    "4": (DeadlyTrap, EpicTrap, DangerousTrap),
    "5": (DeadlyTrap, EpicTrap),
    "6": (LegendaryTrap, EpicTrap),
}, key_bias="front_linear", val_bias="front_linear")


def random_trap(cr, dam_type=None):
    tier = str(CR(cr).tier)
    return random_trap_by_tier(tier, cr, dam_type)


if __name__ == "__main__":
    print()
    for i in range(-3, 31):
        print(random_trap(i))

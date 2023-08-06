from Fortuna import smart_clamp, TruffleShuffle


__all__ = ("CR", "monster_stats", "random_monster_type")


class CR:

    def __init__(self, val):
        self.val = smart_clamp(val, -3, 30)

    @property
    def value(self):
        return self.val

    @property
    def key(self):
        return self.val + 3

    @property
    def string(self):
        if self.val > 0:
            str_cr = f"{self.val}"
        else:
            str_cr = ("1/16", "1/8", "1/4", "1/2")[self.key]
        return str_cr

    @property
    def tier(self):
        return (
            0, 0, 0, 0,
            1, 1, 1, 1, 1,
            2, 2, 2, 2, 2,
            3, 3, 3, 3, 3,
            4, 4, 4, 4, 4,
            5, 5, 5, 5, 5,
            6, 6, 6, 6, 6,
        )[self.key]

    @classmethod
    def party_adapter(cls, average_level, num_players=5, difficulty=0):
        average_level = smart_clamp(average_level, 1, 20)
        num_players = smart_clamp(num_players, 1, 9) - 5
        magic_bonus = (
            0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4,
        )[average_level]
        diff_modifier = smart_clamp(difficulty, -5, 5)
        return num_players + average_level + magic_bonus + diff_modifier

    def __str__(self):
        return self.string

    def __add__(self, other):
        self.val = smart_clamp(self.val + other, -3, 30)
        return self

    def __sub__(self, other):
        self.val = smart_clamp(self.val - other, -3, 30)
        return self


monster_stats = {
    "AC": (
        8, 9, 10, 11,
        11, 12, 13, 14, 14, 15, 15, 16, 16, 17,
        17, 17, 18, 18, 18, 18, 19, 19, 19, 19,
        19, 20, 20, 20, 20, 20, 21, 21, 21, 22,
    ),
    "ATT": (
        0, 1, 2, 3,
        3, 3, 4, 5, 5, 6, 6, 7, 7, 7,
        8, 8, 8, 9, 9, 9, 9, 10, 10, 10,
        11, 11, 11, 12, 12, 12, 13, 13, 13, 14,
    ),
    "HP Range": (
        (1, 7), (7, 36), (36, 50), (50, 71),
        (71, 86), (86, 101), (101, 116), (116, 131), (131, 146),
        (146, 161), (161, 176), (176, 191), (191, 206), (206, 221),
        (221, 236), (236, 251), (251, 266), (266, 281), (281, 296),
        (296, 311), (311, 326), (326, 341), (341, 356), (356, 401),
        (401, 446), (446, 491), (491, 536), (536, 581), (581, 626),
        (626, 671), (671, 716), (716, 761), (761, 806), (806, 851),
    ),
    "DC": (
        13, 13, 13, 13,
        13, 13, 13, 14, 15, 15, 15, 16, 16, 16,
        17, 17, 18, 18, 18, 18, 19, 19, 19, 19,
        20, 20, 20, 21, 21, 21, 22, 22, 23, 24,
    ),
    "Damage Range": (
        (1, 2), (2, 3), (4, 5), (6, 8),
        (9, 14), (15, 20), (21, 26), (27, 32), (33, 38),
        (39, 44), (45, 50), (51, 56), (57, 62), (63, 68),
        (69, 74), (75, 80), (81, 86), (87, 92), (93, 98),
        (99, 104), (105, 110), (111, 116), (117, 122), (123, 140),
        (141, 158), (159, 176), (177, 194), (195, 212), (213, 230),
        (231, 248), (249, 266), (267, 284), (285, 302), (303, 320),
    ),
    "XP": (
        10, 25, 50, 100,
        200, 450, 700, 1100, 1800,
        2300, 2900, 3900, 5000, 5900,
        7200, 8400, 10000, 11500, 13000,
        15000, 18000, 20000, 22000, 25000,
        33000, 41000, 50000, 62000, 155000,
        155000, 155000, 155000, 155000, 155000,
        155000, 155000, 155000, 155000, 155000,
    ),
}


monster_types = (
    "Aberration",
    "Beast",
    "Celestial",
    "Construct",
    "Dragon",
    "Elemental",
    "Fey",
    "Fiend",
    "Giant",
    "Humanoid",
    "Monstrosity",
    "Plant",
    "Ooze",
    "Undead",
)

random_monster_type = TruffleShuffle(monster_types)


if __name__ == '__main__':
    from MonsterGen import CR

    print(f"CR: {CR(-3)}")
    print(f"CR: {CR(-2)}")
    print(f"CR: {CR(-1)}")
    print(f"CR: {CR(0)}")
    print(f"CR: {CR(1)}")
    print(f"CR: {CR(2)}")
    print(f"CR: {CR(3)}")
    print('...')
    print(f"CR: {CR(30)}")

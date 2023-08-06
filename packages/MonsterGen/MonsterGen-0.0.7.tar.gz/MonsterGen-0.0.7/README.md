# MonsterGen

MonsterGen is based on Fortuna and Storm by Robert Sharp.
- Fortuna: Random Value Toolkit for Generative Modeling.
- Storm: High-performance Random Number Engine.


## Installation
```shell script
$ pip install MonsterGen
```

## Index
- CR
- Random Monsters
- Random NPCs
- Random Traps
- Random Treasure


## CR Class
`CR(cr) -> CR`
- cr: required int, -3 to 30

The CR class is a numeric system representing the relative power of a monster in D&D 5e.
This system is a bit funky with values below 1, be careful... here be dragons!
CR less than 1 are printed as fractions but valued mathematically as integers [-3, 0]. See below:

### CR Mapping

```python
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
```

```
CR: 1/16
CR: 1/8
CR: 1/4
CR: 1/2
CR: 1
CR: 2
CR: 3
...
CR: 30
```

### Party Adapter Class Method
`CR.player_adapter(average_level, num_players=5, difficulty=0) -> CR`

Class method for computing CR from party composition and difficulty setting.
- average_level: required int, 1 to 20
- num_players: optional int, 1 to 9
- difficulty: optional int, -5 to 5 
    - Stupid Easy: -5 to -4
    - Easy: -3 to -2
    - Normal: -1 to 1
    - Epic: 2 to 3
    - Legendary: 4 to 5


## Monster Class
`Monster(cr, monster_type=None) -> Monster`

- cr: required int, -3 to 30
- monster_type: optional str, ["Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity", "Plant", "Ooze", "Undead"]

```python
from MonsterGen import Monster, CR

monster_cr = CR(10)
print(Monster(monster_cr, monster_type='Aberration'))
```

```
Name: Grell
Type: Aberration
CR: 7
Hit Points: 164
Armor Class: 12
Attack Bonus: 9
Typical Damage: 45 - 50
Save DC: 15
XP Value: 2900
```

## NPC Class
`Npc() -> Npc`

Produces a random NPC.

```python
from MonsterGen import Npc

print(Npc())
```

```
Profession: Bookbinder
Race: Tiefling
Background: Soldier
Appearance: Flamboyant or outlandish clothes
Mannerism: Speaks in rhyme
Hit Points: 8
Armor Class: 11
Damage: 1
```

## Random Trap Factory Function
`random_trap(cr, dam_type=None) -> Trap`
- cr: required int, -3 to 30
- dam_type: optional str, ['bludgeoning', 'falling', 'piercing', 'slashing', 'poison', 'acid', 'fire', 'lightning', 'cold', 'necrotic']

Produces a random trap. If `dam_type` is None it will choose a random damage type.

```python
from MonsterGen import random_trap

print(random_trap(10, dam_type="fire"))
```

```
Name: Inferno
Type: Minor Trap
CR: 10
Spot & Disarm: DC: 10
Save vs: WIS DC 11 for half damage
Damage: 3d4 fire
Disarm XP: 5900
```

## Monster Loot Factory Function
`monster_loot(cr) -> Loot`
- cr: required int, -3 to 30

Produces random treasure for a single monster. Typically this is just coinage.
```python
from MonsterGen import monster_loot

print(monster_loot(10))
```

```
Copper Coins: 1800
Electrum Coins: 50
```

## Horde Loot Factory Function
`horde_loot(cr) -> Loot`
- cr: required int, -3 to 30

Produces random treasure for a boss or horde of monsters. High-quality loot with magic items appropriate to the CR.

```python
from MonsterGen import horde_loot

print(horde_loot(10))
```

```
Copper Coins: 400
Silver Coins: 7000
Gold Coins: 2200
Platinum Coins: 140
Jewels: 50 GP
Oil of etherealness
Quaal's feather token
```

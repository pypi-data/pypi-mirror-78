from Fortuna import FlexCat


__all__ = ("random_monster_by_type", )


random_monster_by_type = FlexCat({
    'Aberration': [
        'Aboleth', 'Beholder', 'Spectator', 'Chuul', 'Cloaker',
        'Flumph', 'Gibbering Mouther', 'Grell', 'Intellect Devourer',
        'Mind Flayer', 'Mind Flayer Arcanist', 'Nothic', 'Otyugh',
        'Slaad Tadpole', 'Red Slaad', 'Blue Slaad', 'Green Slaad',
        'Gray Slaad', 'Death Slaad',
    ],
    'Beast': [
        'Allosaurus', 'Ankylosaurus', 'Pteranodon', 'Plesiosaurus',
        'Triceratops', 'Tyrannosaurus Rex', 'Stirge', 'Axe Beak', 'Ape',
        'Baboon', 'Badger', 'Bat', 'Black Bear', 'Blood Hawk', 'Boar',
        'Brown Bear', 'Cat', 'Crab', 'Camel', 'Constrictor Snake',
        'Crocodile', 'Deer', 'Draft Horse', 'Dire Wolf', 'Frog', 'Eagle',
        'Flying Snake', 'Elk', 'Elephant', 'Giant Badger', 'Giant Bat',
        'Giant Centipede', 'Giant Boar', 'Giant Ape', 'Giant Crab',
        'Giant Eagle', 'Giant Constrictor Snake', 'Giant Crocodile',
        'Giant Fire Beetle', 'Giant Frog', 'Giant Elk', 'Giant Lizard',
        'Giant Goat', 'Giant Hyena', 'Giant Octopus', 'Giant Rat',
        'Giant Owl', 'Giant Poisonous Snake', 'Giant Scorpion',
        'Giant Sea Horse', 'Giant Spider', 'Giant Shark', 'Giant Weasel',
        'Giant Wasp', 'Giant Toad', 'Giant Vulture', 'Goat', 'Hawk',
        'Giant Wolf Spider', 'Hunter Shark', 'Hyena', 'Jackal', 'Lion',
        'Killer Whale', 'Lizard', 'Mastiff', 'Mammoth', 'Octopus', 'Owl',
        'Mule', 'Panther', 'Poisonous Snake', 'Cave Bear', 'Polar Bear',
        'Quipper', 'Rat', 'Raven', 'Pony', 'Riding Horse', 'Reef Shark',
        'Rhinoceros', 'Saber-toothed Tiger', 'Sea Horse', 'Scorpion',
        'Spider', 'Swarm of Bats', 'Swarm of Insects',
        'Swarm of Quippers', 'Swarm of Poisonous Snakes', 'Vulture',
        'Swarm of Rats', 'Swarm of Ravens', 'Tiger', 'Weasel', 'Warhorse',
        'Wolf',
    ],
    'Celestial': [
        'Deva', 'Planetar', 'Solar', 'Couatl', 'Empyrean', 'Pegasus',
        'Unicorn',
    ],
    'Construct': [
        'Animated Armor', 'Flying Sword', 'Rug of Smothering',
        'Clay Golem', 'Flesh Golem', 'Stone Golem', 'Iron Golem',
        'Helmed Horror', 'Homunculus', 'Monodrone', 'Duodrone',
        'Tridrone', 'Quadrone', 'Pentadrone', 'Scarecrow',
        'Shield Guardian',
    ],
    'Dragon': [
        'Young Red Shadow Dragon', 'Ancient Black Dragon',
        'Black Dragon Wyrmling', 'Young Black Dragon',
        'Adult Black Dragon', 'Ancient Blue Dragon',
        'Blue Dragon Wyrmling', 'Young Blue Dragon', 'Adult Blue Dragon',
        'Ancient Green Dragon', 'Young Green Dragon',
        'Adult Green Dragon', 'Green Dragon Wyrmling',
        'Ancient Red Dragon', 'Red Dragon Wyrmling', 'Young Red Dragon',
        'Adult Red Dragon', 'Ancient White Dragon', 'Young White Dragon',
        'Adult White Dragon', 'White Dragon Wyrmling',
        'Ancient Brass Dragon', 'Young Brass Dragon',
        'Adult Brass Dragon', 'Brass Dragon Wyrmling',
        'Ancient Bronze Dragon', 'Young Bronze Dragon',
        'Adult Bronze Dragon', 'Bronze Dragon Wyrmling',
        'Ancient Copper Dragon', 'Young Copper Dragon',
        'Adult Copper Dragon', 'Copper Dragon Wyrmling',
        'Ancient Gold Dragon', 'Adult Gold Dragon',
        'Gold Dragon Wyrmling', 'Young Gold Dragon',
        'Ancient Silver Dragon', 'Adult Silver Dragon',
        'Silver Dragon Wyrmling', 'Young Silver Dragon', 'Dragon Turtle',
        'Young Faerie Dragon', 'Adult Faerie Dragon', 'Pseudodragon',
        'Wyvern',
    ],
    'Elemental': [
        'Azer', 'Air Elemental', 'Earth Elemental', 'Fire Elemental',
        'Water Elemental', 'Galeb Duhr', 'Gargoyle', 'Dao', 'Djinni',
        'Efreeti', 'Marid', 'Invisible Stalker', 'Magmin',
        'Dust Mephit', 'Ice Mephit', 'Mud Mephit', 'Magma Mephit',
        'Smoke Mephit', 'Steam Mephit', 'Fire Snake', 'Salamander',
        'Water Weird', 'Xorn',
    ],
    'Fey': [
        'Dryad', 'Green Hag', 'Sea Hag', 'Pixie', 'Satyr', 'Sprite',
        'Blink Dog',
    ],
    'Fiend': [
        'Cambion', 'Balor', 'Barlgura', 'Dretch', 'Chasme', 'Glabrezu',
        'Goristro', 'Manes', 'Hezrou', 'Marilith', 'Nalfeshnee', 'Quasit',
        'Shadow Demon', 'Vrock', 'Yochlol', 'Bearded Devil',
        'Barbed Devil', 'Bone Devil', 'Chain Devil', 'Erinyes',
        'Horned Devil', 'Ice Devil', 'Lemure', 'Imp', 'Pit Fiend',
        'Spined Devil', 'Gnoll Fang of Yeenoghu', 'Night Hag',
        'Hell Hound', 'Nightmare', 'Rakshasa', 'Incubus', 'Succubus',
        'Mezzoloth', 'Arcanaloth', 'Nycaloth', 'Ultroloth',
    ],
    'Giant': [
        'Cyclops', 'Ettin', 'Fomorian', 'Cloud Giant', 'Fire Giant',
        'Hill Giant', 'Frost Giant', 'Stone Giant', 'Storm Giant', 'Ogre',
        'Half Ogre', 'Oni', 'Troll',
    ],
    'Humanoid': [
        'Aarakocra', 'Bugbear', 'Bugbear Chief', 'Bullywug', 'Duergar',
        'Drow', 'Drow Elite Warrior', 'Drow Mage',
        'Drow Priestess of Lolth', 'Githyanki Warrior',
        'Githyanki Knight', 'Githzerai Monk', 'Githzerai Zerth',
        'Gnoll', 'Gnoll PackLord', 'Svirfneblin', 'Goblin',
        'Goblin Boss', 'Grimlock', 'Half Red Dragon Veteran',
        'Hobgoblin', 'Hobgoblin Captain', 'Hobgoblin Warlord',
        'Jackalwere', 'Kenku', 'Kobold', 'Winged Kobold', 'Kuo-toa',
        'Kuo-toa Whip', 'Kuo-toa Archpriest', 'Lizardfolk',
        'Lizardfolk Shaman', 'Lizard King', 'Lizard Queen', 'Werebear',
        'Wererat', 'Wereboar', 'Weretiger', 'Werewolf', 'Merfolk',
        'Orc', 'Orc War Chief', 'Orc Eye of Gruumsh', 'Orog',
        'Quaggoth', 'Quaggoth Thonot', 'Sahuagin',
        'Sahuagin Priestess', 'Sahuagin Baron', 'Thri-kreen',
        'Troglodyte', 'Yuan-ti Pureblood',
    ],
    'Monstrosity': [
        'Ankheg', 'Basilisk', 'Behir', 'Bulette', 'Carrion Crawler',
        'Centaur', 'Chimera', 'Cockatrice', 'Darkmantle',
        'Displacer Beast', 'Doppelganger', 'Drider', 'Ettercap',
        'Gorgon', 'Grick', 'Grick Alpha', 'Griffon', 'Harpy',
        'Hippogriff', 'Hook Horror', 'Hydra', 'Kraken', 'Lamia',
        'Manticore', 'Medusa', 'Merrow', 'Mimic', 'Minotaur',
        'Spirit Naga', 'Guardian Naga', 'Owlbear', 'Peryton',
        'Piercer', 'Purple Worm', 'Young Remorhaz', 'Remorhaz',
        'Roc', 'Roper', 'Rust Monster', 'Androsphinx', 'Gynosphinx',
        'Tarrasque', 'Umber Hulk', 'Yeti', 'Abominable Yeti',
        'Yuan-ti Abomination', 'Yuan-ti Malison', 'Death Dog',
        'Phase Spider', 'Winter Wolf', 'Worg',
    ],
    'Plant': [
        'Twig Blight', 'Needle Blight', 'Vine Blight', 'Shrieker',
        'Violet Fungus', 'Gas Spore', 'Myconid Sprout',
        'Quaggoth Spore Servant', 'Myconid Adult', 'Myconid Sovereign',
        'Shambling Mound', 'Treant', 'Awakened Shrub', 'Awakened Tree',
    ],
    'Ooze': [
        'Black Pudding', 'Gelatinous Cube', 'Gray Ooze', 'Ochre Jelly',
        'Gelatinous Sphere', 'Green Slime', 'Sewer Moss',
    ],
    'Undead': [
        'Banshee', 'Death Tyrant', 'Crawling Claw', 'Death Knight',
        'Demilich', 'Dracolich', 'Flameskull', 'Ghost',
        'Ghoul', 'Ghast', 'Lich', 'Mummy', 'Mummy Lord', 'Bone Naga',
        'Revenant', 'Shadow', 'Skeleton', 'Warhorse Skeleton',
        'Minotaur Skeleton', 'Specter', 'Poltergeist', 'Vampire',
        'Vampire Caster', 'Vampire Warrior', 'Vampire Spawn', 'Wight',
        'Will-o-wisp', 'Wraith', 'Zombie', 'Ogre Zombie',
        'Beholder Zombie',
    ],
}, key_bias="truffle_shuffle")


if __name__ == '__main__':
    monster_choice = "Undead"
    if monster_choice in random_monster_by_type.cat_keys:
        for _ in range(10):
            print(random_monster_by_type(monster_choice))
    else:
        for _ in range(10):
            print(random_monster_by_type())

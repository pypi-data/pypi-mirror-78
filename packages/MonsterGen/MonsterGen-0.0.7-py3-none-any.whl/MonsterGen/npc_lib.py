from Fortuna import QuantumMonty, TruffleShuffle


__all__ = (
    "random_human", "random_race", "random_appearance", "random_mannerism",
    "random_profession", "random_background",
)


random_human = QuantumMonty((
    "Human Peasant",
    "Human Villager",
    "Human Highborn",
    "Human Outcast",
    "Human Noble",
    "Human Outlaw",
    "Human Royal",
)).front_gauss

random_race = TruffleShuffle((
    random_human, "Mountain Dwarf", "Hill Dwarf", "Shout Halfling",
    "Lightfoot Halfling", "Forest Gnome", "Rock Gnome", "High Elf",
    "Wood Elf", "Half-elf", "Drow", "Half-orc", "Tiefling", "Dragonborn",
))

random_appearance = TruffleShuffle((
    "Distinctive jewelry", "Piercings", "Flamboyant or outlandish clothes",
    "Formal, clean clothes", "Ragged, dirty clothes", "Pronounced scar",
    "Missing teeth", "Missing fingers", "Unusual eye color", "Tattoos",
    "Birthmark", "Unusual skin color", "Bald", "Braided beard or hair",
    "Unusual hair color", "Nervous eye twitch", "Distinctive nose",
    "Exceptionally ugly", "Distinctive posture", "Exceptionally beautiful",
))

random_mannerism = TruffleShuffle((
    "Prone to singing", "Prone to whistling", "Prone to humming quietly",
    "Speaks in rhyme", "Speaks in some peculiar way",
    "Particularly low booming voice", "High-pitched screechy voice",
    "Slurs words", "Enunciates overly clearly", "Speaks with a lisp",
    "Speaks with a stutter", "Speaks loudly", "Whispers", "Uses flowery speech",
    "Uses unnecessarily long words", "Frequently uses the wrong word",
    "Uses colorful oaths and exclamations", "Makes constant jokes or puns",
    "Prone to predictions of doom", "Fidgets", "Squints",
    "Stares into the distance", "Chews something",
    "Paces", "Taps fingers", "Bites fingernails",
    "Twirls hair or tugs beard",
))

random_profession = TruffleShuffle((
    "Acrobat", "Animal Trainer", "Armor Smith", "Baker", "Barmaid",
    "Barber", "Bartender", "Blacksmith", "Bookbinder", "Bowyer Fletcher",
    "Brewer", "Butcher", "Butler", "Candlestick Maker", "Chef", "Clerk",
    "Jester", "Courtesan", "Dancer", "Farrier", "Ferryman", "Fire Eater",
    "Fisherman", "Fool", "Fortuneteller", "Gardener", "Gatekeeper",
    "Glassblower", "Hatter", "Healer", "Herbalist", "Innkeeper",
    "Jailer", "Juggler", "Lamp Wright", "Leather Worker", "Locksmith",
    "Lumberjack", "Merchant", "Missionary", "Mortician", "Musician",
    "Oracle", "Playwright", "Poet", "Potion Salesman", "Potter",
    "Prostitute", "Quartermaster", "Sailor", "Scholar", "Scout", "Scribe",
    "Sculptor", "Sentry", "Ship Captain", "Shipwright", "Silver Smith",
    "Singer", "Songwriter", "Spice Dealer", "Stage Hand",
    "Stonemason", "Storyteller", "Tailor", "Teacher", "Tracker", "Trapper",
    "Weaver", "Wet Nurse", "Wine Vintner", "Weapon Smith",
))

random_background = TruffleShuffle((
    "Acolyte",
    "Charlatan",
    "Criminal",
    "Entertainer",
    "FolkHero",
    "GuildArtisan",
    "Hermit",
    "Noble",
    "Outlander",
    "Sage",
    "Sailor",
    "Soldier",
    "Urchin",
))

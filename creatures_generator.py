class Creature:
    def __init__(self, character_manager, level):
        self.character_manager = character_manager
        with open('creatures.json', 'r') as f:
            data = json.load(f)
            creatures = random.choice(data['creatures'])
            self.name = f"{creatures['adjectives'][random.randint(0, len(creatures['adjectives']) - 1)]} {creatures['nouns'][random.randint(0, len(creatures['nouns']) - 1)]}"
            self.symbol = creatures['symbol']
            self.level = level
            self.health = creatures['health'] * level
            self.attack = creatures['attack'] * level
            self.defense = creatures['defense'] * level

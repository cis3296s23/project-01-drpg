class CharacterManager:
    def __init__(self, str, end, dex, hp, maxHP, xp, lvl, souls, weapon=None, armor=None):
        self.str = str
        self.end = end
        self.dex = dex
        self.hp = hp
        self.maxHP = maxHP
        self.xp = xp
        self.lvl = lvl
        self.souls = souls
        self.weapon = weapon
        self.armor = armor

    def calc_damage_dealt(self):
        if self.weapon is None:
            return self.str
        else:
            return self.str + (self.weapon.damage * self.weapon.speed)

    def calc_damage_taken(self, damage):
        if self.armor is None:
            return damage * (1 - self.end/100)
        else:
            return damage * (1 - (self.armor.protection / 100)) * (1 - (self.end / 100))

    def modifyHP(self, amount):
        if amount > self.hp:
            self.hp = 0
        else:
            self.hp -= amount  # reduce hp based on calc_damage_taken

    def increaseHP(self, amount):
        if (amount + self.hp) > self.maxHP:
            self.hp = self.maxHP
        else:
            self.hp += amount

    def give_xp(self, amount):  # attain xp
        self.xp += amount

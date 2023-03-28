import bot
import responses
# import gear_generation

class CharacterManager:
    def __init__(self, str, end, dex, hp, xp, lvl, weapon=None, armor=None):
        self.str = str
        self.end = end
        self.dex = dex
        self.hp = hp
        self.lvl = lvl
        self.weapon = weapon
        self.armor = armor

    def calc_damage_dealt(self):
        # depending on the scaling of weapon, dex or str, for now we assume str
        # return self.str + self.weapon.damage
        return self.str     # for now we will use the user's raw strength, meaning pure hands, bro will be swinging like crazy

    def calc_damage_taken(self, damage):
        # if self.armor
            # return (damage * (1 - (self.armor.protection/100))) # damage - armor damage reduction
        # else
        return damage

    def modifyHP(self, damage):
        self.hp -= self.calc_damage_taken(damage)   # reduce hp based on calc_damage_taken

    def check_lvl_up(self):
        # to be decided
        return True

    def give_xp(self, amount):  # attain xp
        self.xp += amount
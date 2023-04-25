# import gear_generation

class CharacterManager:
    def __init__(self, str, end, dex, hp, maxHP, xp, lvl, weapon=None, armor=None):
        self.str = str
        self.end = end
        self.dex = dex
        self.hp = hp
        self.maxHP = maxHP
        self.xp = xp
        self.lvl = lvl
        self.weapon = weapon
        self.armor = armor

    def calc_damage_dealt(self):
        # depending on the scaling of weapon, dex or str, for now we assume str
        # return self.str + self.weapon.damage
        return self.str     # for now we will use the user's raw strength, meaning pure hands, bro will be swinging like crazy

    def calc_damage_taken(self, damage):
        # if self.armor
            # return (damage * (1 - (self.armor.protection/100)) * (1 - (self.end/100)))
        # else
        return damage * (1 - self.end/100)

    def modifyHP(self, amount):
        if amount > self.hp:
            self.hp = 0
        else:
            self.hp -= amount  # reduce hp based on calc_damage_taken

    def check_lvl_up(self):
        if self.xp >= (self.level * 10):   # xp system, increases based on players level
            self.level += 1
            self.xp -= (self.level * 10)
            choice = input("Level up! Please choose a stat to increase: ")
            match choice:   # for every level up, the user gets to choose which stat to increase
                case "str":
                    self.str += 1
                case "end":
                    self.end += 1
                case "dex":
                    self.dex += 1
                case "hp":
                    self.hp += 1
                case _:   # user will be prompted if none of the valid choice are typed
                    print("Invalid stat, please try again")
            return True   # return true if user levels up else return false
        else:
            return False

    def give_xp(self, amount):  # attain xp
        self.xp += amount

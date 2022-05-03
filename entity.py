class Enemy:
    def __init__(self, enemy):
        self.__name = enemy["name"]
        self.__hp = enemy["hp"]
        self.__dmg = enemy["dmg"]
        self.__xp_reward = enemy["xp_reward"]

    def return_info(self):
        return {"Feind": self.__name, "Hp": self.__hp, "Dmg": self.__dmg}

    def attacked(self, damage):
        print("a")
        self.__hp -= damage

    def return_hp(self):
        return self.__hp

    def return_damage(self):
        return self.__dmg

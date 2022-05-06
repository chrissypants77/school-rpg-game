class Enemy:
    def __init__(self, enemy):
        self.__name = enemy["name"]
        self.__hp = enemy["Hp"]
        self.__dmg = enemy["Schaden"]
        self.__xp_reward = enemy["xp_reward"]
        self.__hp_reward = enemy["Hp"]

    def return_info(self, language_dictionary):
        return {language_dictionary["return_info"][0]: self.__name,
                language_dictionary["return_info"][1]: self.__hp,
                language_dictionary["return_info"][2]: self.__dmg}

    def attacked(self, damage):
        self.__hp -= damage

    def return_hp(self):
        return self.__hp

    def return_xp_reward(self):
        return self.__xp_reward

    def return_damage(self):
        return self.__dmg

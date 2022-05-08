class Player:
    def __init__(self, name, load_data=None):

        self.__xp_to_next_level = 10

        if load_data is not None:
            self.name = load_data["name"]
            self.__level = load_data["level"]
            self.__inventory = load_data["inventory"]
            self.__tutorial = load_data["tutorial"]
            self.__settings = load_data["settings"]
            self.__xp = load_data["xp"]
            self.__xp_to_next_level = load_data["xp_to_next_level"]
            self.__damage = 5 + self.__level
            self.__hp = int(load_data["hp"])
            self.__maxhp = load_data["maxhp"]
            self.__clas_name = load_data["clas_name"]
            self.__total_endless_kills = load_data["total_endless_kills"]

        else:
            self.name = name
            self.__world_level = 0
            self.__level = 0

            self.__inventory = {"Potion": {"health potion": 0}}

            self.__tutorial = "disabled"

            self.__xp = 0
            self.__hp = int()
            self.__maxhp = int()
            self.__damage = int()
            self.__clas_name = str()

            self.__total_endless_kills = int()

    def used_heal_potion(self):
        self.__hp += 20
        if self.__hp <= self.__maxhp:
            self.__hp = self.__maxhp

    def attacked(self, damage):
        self.__hp = self.__hp - damage

    def update_language(self, lang):
        self.__settings["Language"] = lang

    def add_endless_kill(self):
        self.__total_endless_kills += 1

    def add_inventory(self, item_genre, item, amount):
        self.__inventory[item_genre][item] += amount

    def level_up(self):
        self.__maxhp += 5
        self.__damage += 1
        self.__level += 1
        self.replenish_hp(True)

    def add_xp(self, xp):
        self.__xp += xp
        if self.__xp >= self.__xp_to_next_level:
            self.level_up()
            self.__xp_to_next_level = ((self.__level / self.__xp*2) * self.__xp_to_next_level) + self.__xp_to_next_level
            self.__xp_to_next_level = round(self.__xp_to_next_level)
            self.__xp = 0

    def replenish_hp(self, max=0):
        if max is True:
            self.__hp = self.__maxhp
            return
        self.__hp += max

    def player_stats_from_clas(self, clas, clas_name):
        self.__hp = clas[0]
        self.__maxhp = clas[1]
        self.__damage = clas[2]
        self.__clas_name = clas_name

    def return_inventory(self):
        return self.__inventory

    def return_damage(self):
        return self.__damage

    def return_hp(self):
        return self.__hp

    def return_player_info(self, language_dictionary):
        # Class
        # Hp
        # Damage
        # Level
        # Xp
        #  of
        return {language_dictionary["return_player_info"][0]: self.__clas_name,
                language_dictionary["return_player_info"][1]: self.__hp,
                language_dictionary["return_player_info"][2]: self.__damage,
                language_dictionary["return_player_info"][3]: self.__level,
                language_dictionary["return_player_info"][4]: str(self.__xp)+language_dictionary["return_player_info"][5]+str(self.__xp_to_next_level)}

    def return_tutorial(self):
        return self.__tutorial

    def return_settings(self):
        return self.__settings

    def return_save(self):
        return {"name": self.name,
                "level": self.__level,
                "inventory": self.__inventory,
                "tutorial": self.__tutorial,
                "settings": self.__settings,
                "xp": self.__xp,
                "xp_to_next_level": self.__xp_to_next_level,
                "damage": self.__damage,
                "hp": self.__hp,
                "maxhp": self.__maxhp,
                "clas_name": self.__clas_name,
                "total_endless_kills": self.__total_endless_kills}

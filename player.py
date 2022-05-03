class Player:
    def __init__(self, name, world_level, level):
        self.name = name

        self.__world_level = world_level
        self.__level = level

        self.__inventory = {"Potion": {"health potion": 0}}

        self.__tutorial = False

        self.__xp = 0
        self.__hp = int()
        self.__maxhp = int()
        self.__damage = int()
        self.__clas_name = str()
        self.__xp_to_next_level = 20

        self.__most_endless_kills = int()

    def used_heal_potion(self):
        self.__hp += 20
        if self.__hp <= self.__maxhp:
            self.__hp = self.__maxhp

    def attacked(self, damage):
        self.__hp = self.__hp - damage

    def add_endless_kill(self):
        self.__most_endless_kills += 1

    def add_inventory(self, item_genre, item, amount):
        self.__inventory[item_genre][item] += amount

    def replenish_hp(self):
        self.__hp = self.__maxhp

    def player_stats_from_clas(self, clas, clas_name):
        self.__hp = clas["hp"]
        self.__maxhp = clas["max_hp"]
        self.__damage = clas["dmg"]
        self.__clas_name = clas_name

    def return_inventory(self):
        return self.__inventory

    def return_damage(self):
        return self.__damage

    def return_hp(self):
        return self.__hp

    def return_player_info(self):
        return {"Klasse": self.__clas_name, "hp": self.__hp, "Schaden": self.__damage}

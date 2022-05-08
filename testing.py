def xp_test():
    level = 1
    xp = 10
    for i in range(0, 20):
        if level <= 20:
            xp = ((level/25) * xp) + xp
            xp = round(xp)
            print(xp)
            level += 1
    a = {"name": "test", "level": 0, "inventory": {"Potion": {"health potion": 0}}, "tutorial": "normal", "settings": {"language": "deutsch", "TTs": False}, "xp": 0, "hp": 25, "clas_name": "Magier", "most_endless_kills": 0}

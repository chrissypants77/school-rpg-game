import random
from tkinter import *
import player as p
import entity as e
import tutorial as t
import world as w

item_list = []
enemy_dictionary = [{"name": "Zombie", "hp": 30, "dmg": 2, "xp_reward": 2}]
clas_dictionary = {"clas_list": ["Magier"], "Magier": {"hp": 25, "max_hp": 25, "dmg": 5}}
world_info = {"world_count": 1,
              "World_0": {"levels": 2, "command": [t.tutorial_1, t.tutorial_2]},
              "World_1": {"levels": 2, "command": [w.world_1_1, w.world_1_2]}}


# creates a entry widget. needs a return if you want the entry's from the widget
def entry(x, y, width):
    box_var = StringVar()
    box = Entry(textvariable=box_var, width=width)
    box.place(x=x, y=y)
    item_list.append(box)
    return box_var


# creates a label
def label(x, y, text, font=(str(), int(), str()), bg="black", after=False, after_ms=int()):
    global item_list
    l1 = Label(text=text, font=font)
    l1.configure(fg=str(bg))
    l1.place(x=x, y=y)
    if after is True:
        l1.after(after_ms, l1.destroy)
    item_list.append(l1)


# creates a button
def button(x, y, text, command, height=int(), width=int()):
    global item_list
    b = Button(root, text=str(text), command=command, height=height, width=width)
    b.place(x=x, y=y)
    item_list.append(b)


# creates a flip down menu
def option_menu(x, y, items=None):
    if items is None:
        items = ["a"]
    var = StringVar(root)
    var.set(items[0])
    om = OptionMenu(root, var, *items)
    om.place(x=x, y=y)
    item_list.append(om)
    return var


# clears all the tkinter modules on screen
def clear_items():
    global item_list
    for i in item_list:
        i.destroy()


# creates a enemy
def create_entity(entity=random.randint(0, len(enemy_dictionary)-1)):
    global enemy
    enemy = e.Enemy(enemy_dictionary[entity])


# the selection to witch level you would like to play (world-level)
def world_level_options():
    clear_items()
    for a in range(0, world_info["world_count"]+1):
        label(x=a*100, y=10, text="Welt "+str(a), font=("Arial", 12, "bold"))
        for b in range(1, world_info["World_"+str(a)]["levels"]+1):
            button(x=a*100, y=40*b, text="Level: "+str(b), command=world_info["World_"+str(a)]["command"][b-1])


# used to see if your lucky when killing a enemy
def rng(low, high, check):
    num = random.randint(low, high)
    print(num)
    if num == check:
        return True
    return False


# checks the Interaction drop down menu
def check_interaction(om1):
    if om1.get() == "Interaktionen":
        label(10, 200, "Das kannst du nicht auswählen", after=True, after_ms=2000)

    elif om1.get() == "Heilen" and player.return_inventory()["Potion"]["health potion"] == 0:
        label(10, 200, "Du hast kein Heil Trank", after=True, after_ms=2000)

    else:
        interaction(om1)


# puts your inventory into a label
def show_inventory():
    inv = player.return_inventory()
    label(10, 220, "Inventar")
    inv_keys = list(inv.keys())
    inv_keys2 = list(inv["Potion"].keys())
    x = int()
    for i in inv_keys:
        pos = 240+25*x
        label(10, pos, i+": ")
        for y in inv_keys2:
            x += 1
            pos = 240 + 20 * x
            label(20, pos, y+": "+str(inv[i][y]))


# executes the interaction that has been selected
def interaction(om1):
    interactions = {"Angriff": (enemy.attacked(player.return_damage())),
                    "Heilen": player.used_heal_potion}

    interactions.get(om1.get())

    if enemy.return_hp() <= 0:
        if rng(1, 4, 4) is True:
            player.add_inventory("Potion", "health potion", 1)
        player.replenish_hp()
        create_entity()

    else:
        player.attacked(enemy.return_damage())

        if player.return_hp() <= 0:
            player.replenish_hp()
            game_menu(lost=True)

    clear_items()
    endless()


# endless mode
def endless():
    show_inventory()
    # -----
    enemy_info = enemy.return_info()
    enemy_info_keys = list(enemy_info.keys())
    x = int()
    for i in enemy_info_keys:
        label(300, 10 + 25 * x, i + ": " + str(enemy_info[i]))
        x += 1
    # -
    player_info = player.return_player_info()
    player_info_keys = list(player_info.keys())
    x = int()
    for i in player_info_keys:
        label(10, 10 + 25 * x, i + ": " + str(player_info[i]))
        x += 1
    # -----
    label(10, 100, "Was wollen sie machen")
    # -
    options = ["Interaktionen", "Angriff", "Heilen"]
    om1 = option_menu(10, 122, options)
    # -
    button(10, 165, "No Text", lambda: check_interaction(om1))
    # -----
    label(10, 425, str(player.name))
    label(444, 425, "Feind")


# game menu. For in game
def game_menu(lost=False):
    clear_items()
    if lost is True:
        label(10, 100, "You died!", ("Arial", 12, "bold"), "red", True, 3000)
    button(10, 10, "Welt", world_level_options)
    button(50, 10, "Endlos", lambda: (clear_items(), create_entity(), endless()))


# creates a new player
def create_player(e1, e3):
    global player
    player = p.Player(name=e1.get(),
                      world_level=0,
                      level=0)
    player.player_stats_from_clas(clas_dictionary.get(e3.get()), e3.get())

    game_menu()


# checks the name and the class if it is valid
def check_new_name(e1, om1):
    if e1.get() == "" or om1.get() not in clas_dictionary:
        label(10, 100, "Einer deiner Eingaben war Fehlerhaft", ("Arial", 15, "bold"), "red")
        return pre_new_game()
    else:
        create_player(e1, om1)


#  input for your name and class
def pre_new_game():
    # -----
    label(10, 10, "Dein Name ~")
    e1 = entry(10, 35, 10)
    button(10, 70, "Starten", lambda: (clear_items(), check_new_name(e1, om1)))
    # -----
    label(105, 10, "Wählen sie ihr Klasse")
    om1 = option_menu(105, 30, clas_dictionary["clas_list"])


# settings menu
def settings():
    clear_items()
    main_menu()
    label(10, 50, "Coming Soon", ("Arial", 12, "bold"))


# main menu
def menu():
    clear_items()
    main_menu()
    button(10, 50, "Coming Soon", menu)
    button(10, 80, "Neues Spiel", lambda: (clear_items(), pre_new_game()))


# menu selection
def main_menu():
    global command_list

    clear_items()

    button(10, 10, "Haupt Menü", menu)
    button(90, 10, "Einstellungen", settings)


# internal code to get the root for the tkinter window
def get_root():
    return root


# creates the tkinter window and some settings for the window
def main():
    global root
    root = Tk()
    root.geometry("500x450")
    root.resizable(width=False, height=False)

    main_menu()

    root.mainloop()


if __name__ == "__main__":
    main()

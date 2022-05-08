import random
from tkinter import *
import player as p
import entity as e
import os
import ast
import languages.deutsch as deutsch
import languages.english as english
import story_mode as sm
item_list = []
enemy_dictionary = [{"name": "Zombie", "Hp": 30, "Schaden": 2, "xp_reward": 2}]
current_save = None


# saves the progress of your game
def save():
    if current_save is not None:
        with open(current_save, "w") as f:
            f.write(str(player.return_save()))
            f.close()


# creates the world information
def world_info_create():
    global world_info
    world_info = {"world_count": 1,
                  "World_names": ["Tutorial", "Flachland"],
                  "World_0": {"levels": 1, "command": [lambda: (clear_items(),
                                                                sm.tutorial_1(root, language_dictionary),
                                                                player.return_settings()["TTs"])]},
                  "World_1": {"levels": 2, "command": [lambda: (clear_items(),
                                                                sm.level_1_1(root, language_dictionary)),
                                                       lambda: (clear_items(),
                                                                sm.level_1_2(root, language_dictionary))]}}


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
def button(x, y, text, command, height=int(), width=int(), state="normal"):
    global item_list
    b = Button(root, text=str(text), command=command, height=height, width=width, state=state)
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
    item_list.clear()


# creates a enemy
def create_entity(entity=random.randint(0, len(enemy_dictionary)-1)):
    global enemy
    enemy = e.Enemy(enemy_dictionary[entity])


# the selection to witch level you would like to play (world-level)
def world_level_options():
    clear_items()
    button(450, 10, language_dictionary["pre_new_game"][0], lambda: (clear_items(), game_menu()))
    for a in range(0, world_info["world_count"]+1):

        # World
        label(x=a*100, y=10, text=language_dictionary["world_level_options"][0]+str(a), font=("Arial", 12, "bold"))
        for b in range(1, world_info["World_"+str(a)]["levels"]+1):

            # Level:
            button(x=a*100, y=40*b, text=language_dictionary["world_level_options"][1]+str(b), command=world_info["World_"+str(a)]["command"][b-1])


# used to see if your lucky when killing a enemy
def rng(low, high, check):
    num = random.randint(low, high)
    if num == check:
        return True
    return False


# puts your inventory into a label
def show_inventory():
    inv = player.return_inventory()
    label(10, 230, "Inventar")
    inv_keys = list(inv.keys())
    inv_keys2 = list(inv["Potion"].keys())
    x = int()
    for i in inv_keys:
        pos = 250+25*x
        label(10, pos, i+": ")
        for y in inv_keys2:
            x += 1
            pos = 250 + 20 * x
            label(20, pos, y+": "+str(inv[i][y]))


# checks the Interaction drop down menu
def check_interaction(om1):

    # Heal
    if om1.get() == language_dictionary["endless"][1][1] and player.return_inventory()["Potion"]["health potion"] == 0:

        # You don't have a healing potion
        label(100, 200, language_dictionary["check_interaction"][0], after=True, after_ms=2000)

    else:
        interaction(om1)


# executes the interaction that has been selected
def interaction(om1):
    interactions = {language_dictionary["endless"][1][0]: (enemy.attacked(player.return_damage())),
                    language_dictionary["endless"][1][1]: player.used_heal_potion}

    print(om1.get(), language_dictionary["endless"][1][1])
    interactions.get(om1.get())

    if enemy.return_hp() <= 0:
        if rng(1, 4, 4) is True:
            player.add_inventory("Potion", "health potion", 1)

        player.add_xp(enemy.return_xp_reward())
        player.replenish_hp()
        player.add_endless_kill()
        create_entity()

    else:
        player.attacked(enemy.return_damage())

        if player.return_hp() <= 0:
            player.replenish_hp(True)
            clear_items()
            game_menu(lost=True)
            return

    clear_items()
    endless()


# endless mode
def endless():
    show_inventory()
    # -----
    enemy_info = enemy.return_info(language_dictionary)
    enemy_info_keys = list(enemy_info.keys())
    x = int()
    for i in enemy_info_keys:
        label(300, 10 + 25 * x, i + ": " + str(enemy_info[i]))
        x += 1
    # -
    player_info = player.return_player_info(language_dictionary)
    player_info_keys = list(player_info.keys())
    x = int()
    for i in player_info_keys:
        label(10, 10 + 25 * x, i + ": " + str(player_info[i]))
        x += 1

    # what do you want to do?
    label(10, 135, language_dictionary["endless"][0])

    # ["Attack", "Heal"]
    options = language_dictionary["endless"][1]
    om1 = option_menu(10, 157, options)

    # Confirm
    button(10, 200, language_dictionary["endless"][2], lambda: check_interaction(om1))
    label(10, 425, str(player.name))

    # Enemy
    label(444, 425, language_dictionary["endless"][3])


# opens the game settings
def game_settings():

    # Back
    button(455, 10, language_dictionary["game_settings"][0], lambda: (clear_items(), game_menu()))
    option = ["Deutsch", "English"]

    # Choose your language
    label(10, 10, language_dictionary["game_settings"][1])
    languages = option_menu(10, 30, option)

    # Save
    # Saved
    button(10, 70, language_dictionary["game_settings"][2], lambda: (activate_language(languages.get()),
                                                                     label(200, 10, language_dictionary["game_settings"][3])))

    player.update_language(languages.get())


# game menu. For in game
def game_menu(lost=False):
    if lost is True:
        # You died!
        label(10, 100, language_dictionary["game_menu"][2], ("Arial", 12, "bold"), "red", True, 3000)

    # World
    button(10, 10, language_dictionary["game_menu"][0], lambda: (clear_items(), world_level_options()))

    # Endless
    button(55, 10, language_dictionary["game_menu"][1], lambda: (clear_items(),
                                                                 create_entity(),
                                                                 endless()), state=player.return_tutorial())

    # saves your progress
    button(430, 10, language_dictionary["game_menu"][3], lambda: (save()))

    # Settings
    button(10, 50, language_dictionary["game_menu"][4], lambda: (clear_items(), game_settings()))


# creates a new player
def create_player(e1, e3):
    global player
    player = p.Player(name=e1.get())
    player.player_stats_from_clas(clas_dictionary.get(e3.get()), e3.get())

    game_menu()


# checks the name and the class if it is valid
def check_new_name(e1, om1):
    if e1.get() == "" or om1.get() not in clas_dictionary["clas_list"]:

        # One of your entries was Incorrect
        label(10, 100, language_dictionary["check_new_name"][0], ("Arial", 15, "bold"), "red")
        return pre_new_game()
    else:
        create_player(e1, om1)


# input for your name and class
def pre_new_game():
    global clas_dictionary
    clas_dictionary = {"clas_list": [language_dictionary["class"][0]], language_dictionary["class"][0]: [25, 25, 5]}

    # Back
    button(450, 10, language_dictionary["pre_new_game"][0], lambda: (clear_items(), choose_language()))

    # Your name ~
    label(10, 10, language_dictionary["pre_new_game"][1])
    e1 = entry(10, 35, 14)

    # Start
    button(10, 70, language_dictionary["pre_new_game"][2], lambda: (clear_items(), check_new_name(e1, om1)))

    # Choose your class
    label(105, 10, language_dictionary["pre_new_game"][3])

    om1 = option_menu(105, 30, clas_dictionary["clas_list"])


# gets all the texts needed
def languages(lang):
    match lang:
        case "Deutsch":
            return deutsch.text()
        case "English":
            return english.text()


# changes the language of the game
def activate_language(lang):
    global language_dictionary
    language_dictionary = languages(lang)


# gives the language options of the game
def choose_language():
    button(455, 10, "Back", lambda: (clear_items(), menu()))
    option = ["Deutsch", "English"]
    label(10, 10, "Choose the language")
    languages = option_menu(10, 30, option)
    button(10, 70, "Select", lambda: (clear_items(), activate_language(languages.get()), pre_new_game()))


# activates the saved settings
def activate_settings():
    settings = player.return_settings()
    activate_language(settings["Language"])
    # settings["TTs"]


# reads a save file and creates a player with it
def load_save(file=None):
    global player, current_save
    if file is not None:
        current_save = file
        f = open(file, "r")
        content = f.read()
        player_data = ast.literal_eval(content)
        f.close()
        player = p.Player(player_data["name"], player_data)
        activate_settings()


# loads a saved file of the player
def load_menu():
    x = int()
    label(10, 10, "Saves:")
    button(455, 10, "Back", lambda: (clear_items(), menu()))
    for i in os.listdir(str(os.getcwd())+"/saves"):
        if i.endswith(".txt"):
            button(100, 50+x, "Load", lambda: (load_save(str(os.getcwd())+"/saves/"+str(i)), clear_items(), game_menu()))
            label(10, 50+x, i)
            x += 25


# main menu
def menu():
    main_menu()
    button(10, 50, "Load game", lambda: (clear_items(), load_menu()))
    button(10, 80, "New game", lambda: (clear_items(), choose_language()))


# settings menu
def settings():
    main_menu()
    label(10, 50, "Coming Soon", ("Arial", 12, "bold"))


# menu selection
def main_menu():
    global command_list
    world_info_create()
    button(10, 10, "Main menu", lambda: (clear_items(), menu()))
    button(90, 10, "Settings", lambda: (clear_items(), settings()))


# internal code to get the root for the tkinter window
def get_root():
    return root


# creates the tkinter window and some settings for the window
def main():
    global root

    root = Tk()
    root.geometry("500x450")
    root.resizable(width=False, height=False)

    clear_items()
    main_menu()

    root.mainloop()


if __name__ == "__main__":
    main()

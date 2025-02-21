import os
import re

import webbrowser

# Returns a 2D List of game IDs and Names at the given Steam Library Path.
def get_steam_library(library_path):
    games = []

    if not os.path.exists(library_path):
        print("The specified directory does not exist.")
        return games

    for file in os.listdir(library_path):

        if file.startswith("appmanifest") and file.endswith(".acf"):
            file_path = os.path.join(library_path, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    appid_match = re.search(r'"appid"\s+"(\d+)"', content)
                    name_match = re.search(r'"name"\s+"([^"]+)"', content)

                    if appid_match and name_match:
                        appid = appid_match.group(1)
                        name = name_match.group(1)
                        games.append([appid, name])
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return games

def find_launch():

    default_path = os.path.expandvars(r"C:\Program Files (x86)\Steam\steamapps")
    user_path = input(f"Enter your Steam library path (press enter to use default: {default_path}): ").strip()
    if not user_path:
        user_path = default_path

    games = get_steam_library(user_path)
    
    if games:
        print(f"\nInstalled Steam Games at location \"{user_path}\":")
        for i in range(len(games)):
            print(f"{i}.\tName: {games[i][1]}")
        try:
            game_index = int(input("Enter game index for launch: "))
            print(f"Launching game \"{games[game_index][1]}\".")
            webbrowser.open(f"steam://rungameid/{int(games[game_index][0])}")
        except Exception as e:
            print(f"Error with input or game launch: {e}")
    else:
        print("No games found or unable to read the library.")

def mini_launch():
    webbrowser.open("steam://open/minigameslist")

def main():
    print("### WELCOME TO STEAMYLAUNCH! ###")
    opt = input("Use python launcher or steam launcher? (p/s): ")
    if(opt == "p"):
        find_launch()
    elif(opt == "s"):
        mini_launch()
    else:
        print("An error occured. Please relaunch the program.")

if __name__ == "__main__":
    main()

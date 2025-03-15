import os
import re
import webbrowser

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.txt")

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

# Launches a steam game given its game ID.
def launch(launch_id, launch_name=f"by id"):
    current_state = f"Launching game {launch_name}."
    try:
        webbrowser.open(f"steam://rungameid/{int(launch_id)}")
    except Exception as e:
        current_state = f"Error with game launch: {e}"
    return current_state

# QuickLaunch - Launches the Steam game specified for QuickLaunch in settings.
def quick_launch():
    with open(settings_path, "r") as f:
        content = f.read()
        print(launch(content.split("\n")[1]))

# PyLaunch - Opens Steam Library in terminal for selection and launch.
def py_launch():

    # Grab default Library location from settings.
    default_path = os.path.expandvars(r"C:\Program Files (x86)\Steam\steamapps")
    with open(settings_path, "r") as f:
        content = f.read()
        default_path = content.split("\n")[0]

    user_path = input(f"\n(press [ENTER] to use default: {default_path})\nEnter Steam Library Path: ").strip()
    if not user_path:
        user_path = default_path

    games = get_steam_library(user_path)
    
    if games:
        print(f"\nInstalled Steam Games at location \"{user_path}\":")

        # Calculate dynamic widths.
        max_id_length = max(len(str(game[0])) for game in games)
        max_name_length = max(len(game[1]) for game in games)

        # Print with calculated dynamic widths.
        for i in range(len(games)):
            print(f"{i:5}. ID: {str(games[i][0]):<{max_id_length}} Name: {games[i][1]:<{max_name_length}}")
        
        # Try game launch from selection.
        try:
            game_index = int(input("Enter game index for launch: "))
            print(launch(games[game_index][0], games[game_index][1]))
        except Exception as e:
            print(f"Error with input: {e}")
    else:
        print("No games found or unable to read the library.")

# MiniLaunch - Opens Steam's Library in Small Mode.
def mini_launch():
    webbrowser.open("steam://open/minigameslist")

# Settings - Edit default Steam Library location and QuickLaunch ID.
def settings():
    with open(settings_path, "r") as f:
        content = f.read()
        settings_info = content.split("\n")

    new_path = input(f"(press [ENTER] to keep previous: {settings_info[0]})\nEnter New Steam Library Path: ").strip()
    if not new_path:
        new_path = settings_info[0]

    new_id = input(f"(press [ENTER] to keep previous: {settings_info[1]})\nEnter New QuickLaunch Game ID: ").strip()
    if not new_id:
        new_id = settings_info[1]

    with open(settings_path, "w") as f:
        f.write(f"{new_path}\n{new_id}")

# Function Selection
def main():
    print("SteamyLaunch is running...")
    opt = input("PyLaunch, QuickLaunch, MiniLaunch or Settings? (p/q/m/s): ")
    if(opt == "p"):
        py_launch()
    if(opt == "q"):
        quick_launch()
    elif(opt == "m"):
        mini_launch()
    elif(opt == "s"):
        settings()
    else:
        print("An error occured. Please relaunch the program.")

if __name__ == "__main__":
    main()

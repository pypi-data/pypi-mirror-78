import argparse
import os
import steamclient
import json
import requests

# Parse command line flags
parser = argparse.ArgumentParser(description='Manage Steam Shortcuts')
parser.add_argument("--directory", help="location of installed game(s)", required=True)
parser.add_argument("--dry-run", help="don't write any changes", action="store_true")
parser.add_argument("--clear-cache", help="clears the app ID cache", action="store_true")
parser.add_argument("--vr", help="sets VR flag for all games", action="store_true")
parser.add_argument("--artwork", help="gets official artwork from Steam", action="store_true")
parser.add_argument("--overwrite", help="overwrite existing artwork files", action="store_true")
args = parser.parse_args()

# Dry run (don't write changes)
if args.dry_run:
    print("performing dry run (no changes will be made)")

# Directory containing installed game(s)
game_dir = args.directory if args.directory else "./"
if not os.path.isdir(game_dir):
    print(f'error: {game_dir} is not a directory')

# Get Steam IDs and cache the file in apps.json
if os.path.isfile("apps.json") and not args.clear_cache:
    with open("apps.json", "r", encoding="utf-8") as file:
        app_ids = json.load(file)
else:
    with open("apps.json", "w", encoding="utf-8") as file:
        # Get a list of app IDs from Steam Web API
        response = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')
        apps = response.json()['applist']['apps']
        app_ids = {}
        for app in apps:
            # Remove invalid filename characters
            name = "".join(c for c in str(app['name']) if c not in r"\/:*?<>|")
            name = name.replace("\u00ae", "").replace("\u2122", "")
            app_ids[name] = app['appid']

        # Missing for some reason
        app_ids["Vacation Simulator"] = 726830
        app_ids["The Outer Worlds"] = 578650
        
        # Cache to apps.json 
        file.write(json.dumps(app_ids, indent=4))

def get_exe(path, name):
    """ Returns the .exe from a given path or None if not found.
    kind of a mess as I just threw stuff on until all the games I had worked
    """
    
    # Files to ignore (uninstallers)
    exe_blacklist = ["unins000.exe", "unitycrashhandler64.exe", "EasyAntiCheat_launcher.exe"]
    
    # Check every .exe in the directory and pick the best one
    # Make a list of likely names, these will be .lower() later
    likely_names = []
    likely_names.append(name) # Half-Life 2.exe
    likely_names.append(name.replace("-", "")) # HalfLife 2.exe 
    likely_names.append(name.replace(" ", "")) # Half-Life2.exe 
    likely_names.append(name.replace(" ", "").replace("-", "")) # HalfLife2.exe
    acronym = str([word for word in name.split(" ")])
    likely_names.append(acronym) # HL-2.exe
    likely_names.append(acronym.replace("-", "")) # HL2.exe
    
    for likely_name in likely_names:
        if likely_names == "":
            continue
        # Append ".exe" to the filename
        likely_name = likely_name + ".exe"
        
        # Search for the likely filename
        for file in os.listdir(path):
            if file.lower() == likely_name.lower():
                return os.path.join(path, file)
    
    # Find the first .exe in sight
    for name in os.listdir(path):
        if name.lower().endswith('.exe'):
            if not name.lower() in exe_blacklist:
                return os.path.join(path, name)

    # Check some subdirectories for the .exe if we haven't found it yet
    for directory in ["bin", "x64", "MossGame", "Binaries", "Win64", "Game"]:
        dir = os.path.join(path, directory)
        print(f"following {dir}")
        if os.path.isdir(dir):
            exe = get_exe(dir, name)
            if exe is not None:
                return exe

    return None

def get_app_id(game_name):
    """ Returns the Steam app ID or None if not found """
    app_id = None
    
    # See if we get lucky and find it by name
    try:
        app_id = app_ids[game_name]
    except KeyError:
        pass

    return app_id


def main():
    """ this code is such a mess """
    games = []

    # Is this a game or a folder containing a bunch of games?
    # First check if there is an .exe in this folder
    name = os.path.basename(game_dir)
    exe = get_exe(game_dir, name)
    if exe is not None:
        games.append(dict(path=exe, name=name))

    # If we didn't find an .exe in the given directory, assume all subfolders are games.
    if not games:
        for name in os.listdir(game_dir):
            # Skip some subdirectories
            if name in ["VR", "Warcraft III"]:
                continue
            if os.path.isdir(os.path.join(game_dir, name)):
                path = game_dir + name
                games.append(dict(path=path, name=name))

    # Get Steam User info
    user = steamclient.get_users()[0]
    shortcuts = user.shortcuts

    # Keep track of how many things we do
    shortcuts_created = 0
    header_count, grid_count, logo_count = 0, 0, 0
    header_count_skipped, grid_count_skipped, logo_count_skipped = 0, 0, 0
    shortcut_count_dry, header_count_dry, grid_count_dry, logo_count_dry = 0, 0, 0, 0

    # Iterate through each game.
    failed = []
    for game in games:
        print("---------------------------")
        print(f"Name: {game['name']}")

        # Find the executable.
        game['exe'] = get_exe(game['path'], game['name'])
        if game['exe'] is None:
            print(f"Failed to find .exe for {game['name']}")
            failed.append(game)
            continue

        print(f"Exe: {game['exe']}")
        
        # Try to find the steam app ID from the name
        game['app_id'] = get_app_id(game['name'])
        if game['app_id'] is None:
            print(f"Failed to find app_id for {game['name']}")
            failed.append(game)
            continue
            
        # Check if the shortcut exists already.
        shortcut = next((s for s in shortcuts if s.exe.strip('"') == game['exe']), None)

        # Create the shortcut.
        if not shortcut:
            if args.dry_run:
                shortcut_count_dry += 1
            else:                
                print("Creating shortcut:")
                shortcuts_created += 1
                result = user.add_shortcut(
                    name=game['name'],
                    exe=game['exe'],
                    openvr=args.vr
                )
                
                # Returns 0 on success
                if result == 0:
                    shortcuts = user.shortcuts
                    shortcut = next((s for s in shortcuts if s.exe.strip('"') == game['exe']), None)
                else:
                    print(f"Failed to add shortcut for {game['name']}")
                    continue

        # Set artwork to official art from Steam
        if shortcut is not None and args.artwork:
            print("Getting artwork:")
            hero_url = f"https://steamcdn-a.akamaihd.net/steam/apps/{game['app_id']}/library_hero.jpg"
            grid_url = f"https://steamcdn-a.akamaihd.net/steam/apps/{game['app_id']}/library_600x900_2x.jpg"
            logo_url = f"https://steamcdn-a.akamaihd.net/steam/apps/{game['app_id']}/logo.png"
            print(f"header: {hero_url}")
            print(f"grid: {grid_url}")
            print(f"logo: {logo_url}")
            
            if shortcut.has_hero:
                if args.overwrite:
                    if args.dry_run:
                        header_count_dry += 1
                    else: # wet run
                        shortcut.set_hero(url=hero_url)
                        header_count += 1
                else: # don't overwrite
                    header_count_skipped += 1
            else: # shortcut does not have hero
                if args.dry_run:
                    header_count_dry += 1
                else: # wet run
                    shortcut.set_hero(url=hero_url)
                    header_count += 1
                
            if shortcut.has_grid:
                if args.overwrite:
                    if args.dry_run:
                        grid_count_dry += 1
                    else: # wet run
                        shortcut.set_grid(url=grid_url)
                        grid_count += 1
                else: # don't overwrite
                    grid_count_skipped += 1
            else: # shortcut does not have grid
                if args.dry_run:
                    grid_count_dry += 1
                else: # wet run
                    shortcut.set_grid(url=grid_url)
                    grid_count += 1
                
            if shortcut.has_logo:
                if args.overwrite:
                    if args.dry_run:
                        logo_count_dry += 1
                    else: # wet run
                        shortcut.set_logo(url=logo_url)
                        logo_count += 1
                else: # don't overwrite
                    logo_count_skipped += 1
            else: # shortcut does not have logo
                if args.dry_run:
                    logo_count_dry += 1
                else: # wet run
                    shortcut.set_logo(url=logo_url)
                    logo_count += 1

    print("=============================")
    print("Done!")
    print(f"Created {shortcuts_created} new shortcut(s)")
    print(f"Installed:")
    print(f" - {header_count} headers")
    print(f" - {grid_count} grids")
    print(f" - {logo_count} logos")
    if header_count_skipped > 0 or grid_count_skipped > 0 or logo_count_skipped > 0:
        print(f"Skipped due to existing files (use --overwrite to bypass):")
        print(f" - {header_count_skipped} headers")
        print(f" - {grid_count_skipped} grids")
        print(f" - {logo_count_skipped} logos")
    if shortcut_count_dry > 0 or header_count_dry > 0 or grid_count_dry > 0 or logo_count_dry > 0:
        print(f"Skipped due to dry-run (remove --dry-run to write changes):")
        print(f" - {shortcut_count_dry} shortcuts")
        print(f" - {header_count_dry} headers")
        print(f" - {grid_count_dry} grids")
        print(f" - {logo_count_dry} logos")

    print(f"Failed: {len(failed)}")
    for game in failed:
        print(f" - {game['name']}:", end='')
        try:
            if game['app_id'] is None:
                print(" MISSING app_id", end='')
        except:
            print(" MISSING app_id", end='')
        try:
            if game['exe'] is None:
                print(" MISSING exe", end='')
        except:
            print(" MISSING exe", end='')
        print()
        
    print("You may need to restart Steam to see changes!")
    
if __name__ == "__main__":
    main()

import glob
import os
import re
import shutil
import subprocess
import winreg
import zlib

import requests

# Find the Steam install directory or raise an error
try: # 32-bit
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steams")
except FileNotFoundError:
    try: # 64-bit
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam")
    except FileNotFoundError as e:
        print("Failed to find Steam Install directory")
        raise(e)
STEAM_PATH = winreg.QueryValueEx(key, "InstallPath")[0]
_STEAM_KEY = "91597DC019EB19394E3A1E4EB010F025"


class Game():
    """
    Stores the game's ID and name
    """
    def __init__(self, user_id, id, name):
        self.user_id = user_id
        self.id = id
        self.name = name
        
    def __repr__(self):
        return f"<Game {self.name} ({self.id})>"

    @property
    def logo(self):
        """ Returns path to logo on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}_logo.png"

    @property
    def grid(self):
        """ Returns path to cover art on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}p.png"

    @property
    def hero(self):
        """ Returns path to banner on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}_hero.png"
    
    @property
    def has_logo(self):
        """ Returns True if the logo exists on disk """
        return os.path.isfile(self.logo)
    
    @property
    def has_grid(self):
        """ Returns True if the grid exists on disk """
        return os.path.isfile(self.grid)
    
    @property
    def has_hero(self):
        """ Returns True if the hero exists on disk """
        return os.path.isfile(self.hero)

    def set_logo(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is None and url is None:
            raise Exception("Missing filename or url parameter in set_logo() call")
        directory = os.path.dirname(self.logo)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if filepath is not None:
            shutil.copyfile(filepath, self.logo)
        elif url is not None:
            img = requests.get(url).content
            with open(self.logo, 'wb') as f:
                f.write(img)
    
    def set_grid(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is None and url is None:
            raise Exception("Missing filename or url parameter in set_grid() call")
        directory = os.path.dirname(self.grid)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if filepath is not None:
            shutil.copyfile(filepath, self.grid)
        elif url is not None:
            img = requests.get(url).content
            with open(self.grid, 'wb') as f:
                f.write(img)

    def set_hero(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is None and url is None:
            raise Exception("Missing filename or url parameter in set_hero() call")
        directory = os.path.dirname(self.hero)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if filepath is not None:
            shutil.copyfile(filepath, self.hero)
        elif url is not None:
            img = requests.get(url).content
            with open(self.hero, 'wb') as f:
                f.write(img)

class Shortcut(Game):
    """
    A Shortcut is a Game with the additional fields:
    
        user_id:              User ID
        entry_id:             Entry ID
        name:                 Name
        exe:                  Target (quoted path to .exe)
        start_dir:            Start directory (quoted path)
        icon:                 Path to icon
        shortcut_path:        Path to shortcut
        launch_options:       Launch options
        hidden:               Hide from library
        allow_desktop_config: Allow desktop configuration
        allow_overlay:        Allow in-game overlay
        openvr:               Include in VR Library
        devkit:               ?
        devkit_game_id:       ?
        last_play_time:       ?
        tags:                 List of tags
    """
    def __init__(self, user_id, entry_id, name, exe, start_dir=None,
                 icon="", shortcut_path="", launch_options="",
                 hidden=False, allow_desktop_config=True, allow_overlay=True,
                 openvr=False, devkit=False, devkit_game_id="", 
                 last_play_time="\x00\x00\x00\x00", tags=[]):
        self._id = None # calculated below
        self.user_id = user_id
        self.entry_id = entry_id
        self.name = name
        self.exe = '"' + exe.strip('"\'') + '"'
        if start_dir is None:
            self.start_dir = os.path.dirname(self.exe)
        else:
            self.start_dir = '"' + start_dir.strip('"\'') + '"'
        self.icon = icon
        self.shortcut_path = shortcut_path
        self.launch_options = launch_options
        self.hidden = hidden
        self.allow_desktop_config = allow_desktop_config
        self.allow_overlay = allow_overlay
        self.openvr = openvr
        self.devkit = devkit
        self.devkit_game_id = devkit_game_id
        self.last_play_time = last_play_time
        self.tags = tags
    
    def __repr__(self):
        return f"<Shortcut {self.entry_id}: {self.name}>"

    def info(self):
        print(f"Shortcut {self.entry_id}")
        print(f"    id: {self.id}")
        print(f"    name: {self.name}")
        print(f"    exe: {self.exe}")
        print(f"    start_dir: {self.start_dir}")
        print(f'    icon: {self.icon}')
        print(f'    shortcut_path: {self.shortcut_path}')
        print(f'    launch_options: {self.launch_options}')
        print(f"    hidden: {self.hidden}")
        print(f"    allow_desktop_config: {self.allow_desktop_config}")
        print(f"    allow_overlay: {self.allow_overlay}")
        print(f"    openvr: {self.openvr}")
        print(f"    devkit: {self.devkit}")
        print(f"    devkit_game_id: {self.devkit_game_id}")
        print(f"    last_play_time: {self.last_play_time}")
        print(f"    tags: {self.tags}")

    @property
    def id(self):
        """ App ID, used for calculating custom artwork file names """
        if self._id is None:
            s = self.exe + self.name
            self._id = str((zlib.crc32(s.encode()) & 0xffffffff) | 0x80000000)
        return self._id

class User():
    """ User object to store the ID """
    def __init__(self, id):
        """
        Construct a new User object

        :param id: The ID of the user
        """
        self.id = int(id)
        self.comm_id = self.id + 76561197960265728
        """ Community ID """
        self._shortcuts = None
        self._games = None
    
    def __repr__(self):
        return f"<User {self.id}>"


    @property
    def shortcuts(self):
        """ List of Shortcut objects for this user """
        return get_shortcuts(self.id)

    def games(self, libraries=None):
        """ List of Game objects for all local installed games (same for all users) """
        return get_games(self.id, libraries)


    def owned_games(self, include_free=False):
        """ Returns a list of games from the Steam API "GetOwnedGames" endpoint
        "response":{"game_count":147,"games":[
            {"appid":240,"name":"Counter-Strike: Source","playtime_forever":274,"img_icon_url":"9052fa60c496a1c03383b27687ec50f4bf0f0e10","img_logo_url":"ee97d0dbf3e5d5d59e69dc20b98ed9dc8cad5283","has_community_visible_stats":true,"playtime_windows_forever":0,"playtime_mac_forever":0,"playtime_linux_forever":0}
        """
        inc_free = 1 if include_free else 0 # bool to int
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={_STEAM_KEY}&steamid={self.comm_id}&include_appinfo=1&include_played_free_games={inc_free}"
        #print(url)
        req = requests.get(url)
        data = req.json()
        games = []
        for entry in data.get('response', {}).get('games', []):
            games.append(Game(self.id, entry.get('appid'), entry.get('name')))
        return games


    def add_shortcut(self, name, exe, start_dir=None,
                 icon="", shortcut_path="", launch_options="",
                 hidden=False, allow_desktop_config=True, allow_overlay=True,
                 openvr=False, tags=[]):
        """
        Creates a new shortcut (if it does not exist)

        :returns: 0 on success
                  1 if shortcut with same name/exe exists
                  2 if name/exe is empty

        """
        # Validate input
        if name == "" or exe == "":
            return 2

        shortcut = Shortcut(user_id=self.id,
                            entry_id=len(self.shortcuts),
                            name=name,
                            exe=exe,
                            start_dir=start_dir,
                            icon=icon,
                            launch_options=launch_options,
                            hidden=hidden,
                            allow_desktop_config=allow_desktop_config,
                            allow_overlay=allow_overlay,
                            openvr=openvr,
                            tags=tags,
                            )
        for s in self.shortcuts:
            if shortcut.id == s.id:
                # Shortcut with the same name/target exists
                return 1

        # Add to list of shortcuts
        shortcuts_vdf = f"{STEAM_PATH}\\userdata\\{self.id}\\config\\shortcuts.vdf"
        new_entry = create_shortcut_entry(shortcut, entry_id=len(self.shortcuts))
        add_shortcut_entry(shortcuts_vdf, new_entry)
        return 0

def get_games(user_id, libraries=None) -> list:
    """
    Get all of a user's installed games

    :param user_id: the user's ID number
    :param libraries: list of file paths, if None is given - they are all loaded 
    :returns: a list of Game objects
    """
    if libraries is None:
        libraries = get_libraries()

    games = []
    for library in libraries:
        pattern = library + "\\steamapps\\appmanifest_*.acf"
        app_manifests = glob.glob(pattern)
        for manifest in app_manifests:
            app_id = manifest.split('appmanifest_')[-1][:-4]
            name = "Unknown" # placeholder
            with open(manifest, 'r', encoding="utf8") as f:
                while True:
                    line = f.readline()
                    if '"name"' in line:
                        name = line.split('"')[3]
                        break
                    if line == "":
                        break
            games.append(Game(user_id, app_id, name))
    games.sort(key=lambda x: x.name)
    return games

def get_libraries():
    """ 
    Get a list of paths to all Steam Libraries from
    Steam\\steamapps\\libraryfolders.vdf

    :returns: a list of file paths
    """
    libraries = [STEAM_PATH]
    with open(f"{STEAM_PATH}\\steamapps\\libraryfolders.vdf", 'r', encoding="utf8") as f:
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
            re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
    return libraries

def get_shortcuts(user_id):
    """
    Get a user's non-steam Shortcuts from their shortcuts.vdf

    :param user_id: the user's ID number
    :returns: a list of Shortcut objects
    """

    shortcuts_vdf = f"{STEAM_PATH}\\userdata\\{user_id}\\config\\shortcuts.vdf"
    shortcuts = []
    if not os.path.isfile(shortcuts_vdf):
        return shortcuts

    with open(shortcuts_vdf, 'rb') as f:
        header = f.read(11)
        expected = b'\x00shortcuts\x00'
        if header != expected:
            raise Exception(f"Error: first 10 bytes of {shortcuts_vdf} ({header}) are not {expected}")

        # Loop through each shortcut entry
        while True:
            # Check if this is the end of the list
            byte = f.read(1)
            if byte == b'\x08':
                assert f.read(1) ==  b'\x08'
                break

            shortcut = {}
            
            shortcut['entryid'] = _read_id(f)

            # Loop through each variable in the entry
            while True:

                # Data type of the variable
                datatype = f.read(1)
                if datatype == b'\x00': # List
                    key = _read_str(f).decode().lower()
                    val = _read_list(f)
                    shortcut[key] = val
                    break # shortcut entry ends with a list
                elif datatype == b'\x01': # String
                    key = _read_str(f).decode().lower()
                    val = _read_str(f).decode()
                elif datatype == b'\x02': # Boolean
                    key = _read_str(f).decode().lower()
                    if key == "lastplaytime": # this key is weird - only 4 bytes
                        val = f.read(4)
                    else:
                        val = _read_bool(f)
                else:
                    print("Current datatype:")
                    print(datatype)
                    print("Next 30 bytes:")
                    print(f.read(30))
                    raise(Exception(f"Unknown data type while processing shortcuts.vdf: {datatype}"))
                
                #print(f"datatype {datatype} setting {key} to {val}")
                shortcut[key] = val
            
            #print(f"Shortcut dict: {shortcut}")
            s = Shortcut(user_id=user_id,
                         entry_id=shortcut['entryid'], 
                         name=shortcut['appname'],
                         exe=shortcut['exe'],
                         start_dir=shortcut['startdir'],
                         icon=shortcut['icon'],
                         shortcut_path=shortcut['shortcutpath'],
                         launch_options=shortcut['launchoptions'],
                         hidden=shortcut['ishidden'],
                         allow_desktop_config=shortcut['allowdesktopconfig'],
                         allow_overlay=shortcut['allowoverlay'],
                         openvr=shortcut['openvr'],
                         devkit=shortcut['devkit'],
                         devkit_game_id=shortcut['devkitgameid'],
                         last_play_time=shortcut['lastplaytime']
                         )
            shortcuts.append(s)

    return shortcuts

def get_users() -> list:
    """
    Get all users that have logged in.

    :returns: a list of User objects (sorted by last login date)
    """
    users = []
    path = os.path.join(STEAM_PATH, "userdata", "*")
    files = glob.glob(path)
    files.sort(key=os.path.getmtime, reverse=True)
    for file in files:
        basename = os.path.basename(file)
        if basename != "ac" and basename != "0":
            users.append(User(basename))
    return users

# Parsing shortcuts.vdf

def _read_id(f) -> int:
    """
    Helper function for decoding binary files.
    Reads the entry ID from the shortcut entry.
    
    :param f: Open file handler
    :returns: An int
    """
    buffer = b""
    while True:
        byte = f.read(1)
        if byte == b'\x00' or byte == b'':
            break
        buffer += byte
    return int(buffer.decode())

def _read_str(f) -> str:
    """
    Helper function for decoding binary files.
    Reads bytes up until the end of string delimiter or end of file.
    
    :param f: Open file handler
    :returns: A string
    """
    buffer = b""
    delimiter = b'\x00'
    while True:
        byte = f.read(1)
        if byte == delimiter or byte == b'':
            break
        buffer += byte
    return buffer

def _read_bool(f) -> bool:
    """
    Helper function for decoding binary files.
    
    :param f: Open file handler
    :returns: A boolean
    """
    delimiter = b'\x00\x00\x00'
    b = f.read(1)
    assert(f.read(3) == delimiter)
    return True if b == b'\x01' else False

def _read_list(f) -> list:
    """
    Helper function for decoding binary files.
    Reads bytes up until the delimiter or end of file.
    
    :param f: Open file handler
    :returns: A list of strings
    """
    contents = []

    while True:
        byte = f.read(1)
        if byte == b'\x01':
            _read_str(f)
            contents.append(_read_str(f))
        elif byte == b'\x08':
            byte = f.read(1)
            if byte == b'\x08':
                break
            else:
                raise(Exception("_read_list() expected b'\\x08', read {byte}"))

    return contents

def create_shortcut_entry(shortcut, entry_id):
    """ Converts a Shortcut object to an entry.
    Adapted from https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation#shortcut-entry-structure
    """
    hidden = '\x01' if shortcut.hidden else '\x00'
    allow_desktop_config = '\x01' if shortcut.allow_desktop_config else '\x00'
    allow_overlay = '\x01' if shortcut.allow_overlay else '\x00'
    openvr = '\x01' if shortcut.openvr else '\x00'
    devkit = '\x01' if shortcut.devkit else '\x00'

    tags = ""
    for n, tag in enumerate(shortcut.tags):
        if tag != "":
            #print(f"Adding tag {n}: {tag}")
            tags += '\x01' + str(n) + '\x00' + tag + '\x00'
    # Key                # Data Type  # Internal Name       # Delimiter     # Input             # Delimiter
    full_entryID        =                                      '\x00'  +  str(entry_id)                +  '\x00'
    full_appName        =  '\x01'  +  'AppName'             +  '\x00'  +  shortcut.name           +  '\x00'
    full_quotedPath     =  '\x01'  +  'Exe'                 +  '\x00'  +  shortcut.exe            +  '\x00'
    full_startDir       =  '\x01'  +  'StartDir'            +  '\x00'  +  shortcut.start_dir      +  '\x00'
    full_iconPath       =  '\x01'  +  'icon'                +  '\x00'  +  shortcut.icon           +  '\x00'
    full_shortcutPath   =  '\x01'  +  'ShortcutPath'        +  '\x00'  +  shortcut.shortcut_path  +  '\x00'
    full_launchOptions  =  '\x01'  +  'LaunchOptions'       +  '\x00'  +  shortcut.launch_options +  '\x00'
    full_isHidden       =  '\x02'  +  'IsHidden'            +  '\x00'  +  hidden                  +  '\x00\x00\x00'
    full_allowDeskConf  =  '\x02'  +  'AllowDesktopConfig'  +  '\x00'  +  allow_desktop_config    +  '\x00\x00\x00'
    full_allowOverlay   =  '\x02'  +  'AllowOverlay'        +  '\x00'  +  allow_overlay           +  '\x00\x00\x00'
    full_openVR         =  '\x02'  +  'openvr'              +  '\x00'  +  openvr                  +  '\x00\x00\x00'
    full_devkit         =  '\x02'  +  'Devkit'              +  '\x00'  +  devkit                  +  '\x00\x00\x00'
    full_devkitGameID   =  '\x01'  +  'DevkitGameID'        +  '\x00'  +  shortcut.devkit_game_id +  '\x00'
    full_lastPlayTime   =  '\x02'  +  'LastPlayTime'        +  '\x00'  +  shortcut.last_play_time
    full_tags           =  '\x00'  +  'tags'                +  '\x00'  +  tags                    +  '\x08\x08'

    new_entry = full_entryID + full_appName + full_quotedPath + full_startDir + full_iconPath + full_shortcutPath + full_launchOptions + full_isHidden + full_allowDeskConf + full_allowOverlay + full_openVR + full_devkit + full_devkitGameID + full_lastPlayTime + full_tags
    #print("new_entry:", new_entry)
    return new_entry

def add_shortcut_entry(pathToShortcutsVDF, new_entry):
    # https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/blob/master/shortcuts.py#L113-
    if not os.path.isfile(pathToShortcutsVDF):
        with open(pathToShortcutsVDF, 'wb+') as f:
            contents = b'\x00shortcuts\x00\x08\x08'
            f.write(contents)

    # Entries are added before the last two characters of the file
    with open(pathToShortcutsVDF, 'rb+') as f:
        fileContents = f.read()
        f.seek(len(fileContents) - 2)
        endFileContents = f.read()
        f.seek(len(fileContents) - 2)
        data = bytes(new_entry, 'utf8')
        #print("writing:", data)
        f.write(data)
        f.write(endFileContents)


def start_client():
    """ Launches Steam.exe, returns PID """
    path = os.path.realpath(f"{STEAM_PATH}\\Steam.exe")
    #print(f"Launching {path}")
    process = subprocess.Popen(path)
    return process.pid

import os
import toml


CONFIG_FILE = os.path.expanduser("~") + "/.rcl-config"
DEFAULT_CONFIG = {'entries': {}}


def check_install():
    if not os.path.isfile(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)


def save_config(config):
    """ Saves the configuration. OVERWRITES CURRENT CONFIG """
    with open(CONFIG_FILE, "w") as config_file:
        toml.dump(config, config_file)


def load_config():
    """ Loads the configuration. """
    return toml.load(CONFIG_FILE)


def add_entry(entry):
    config = load_config()
    config['entries'][entry['id']] = entry
    save_config(config)


def remove_entry(entry_id):
    config = load_config()
    del config['entries'][entry_id]
    save_config(config)

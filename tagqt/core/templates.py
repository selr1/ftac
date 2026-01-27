import json
import os

TEMPLATES_FILE = os.path.expanduser("~/.config/TagQt/rename_templates.json")


def ensure_config_dir():
    config_dir = os.path.dirname(TEMPLATES_FILE)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)


def save_template(name, pattern):
    ensure_config_dir()
    templates = load_templates()
    templates[name] = pattern
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump(templates, f, indent=2)


def load_templates():
    if os.path.exists(TEMPLATES_FILE):
        try:
            with open(TEMPLATES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "Artist - Title": "%artist% - %title%",
        "Track Title": "%track% %title%",
        "Album - Track Title": "%album% - %track% %title%"
    }


def delete_template(name):
    templates = load_templates()
    if name in templates:
        del templates[name]
        ensure_config_dir()
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, f, indent=2)

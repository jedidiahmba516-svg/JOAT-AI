import json
import os

FILE_NAME = "memory.json"


def load_memory():

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    return {}


def save_memory(memory):

    with open(FILE_NAME, "w") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):

    memory = load_memory()

    memory[key] = value

    save_memory(memory)


def recall(key):

    memory = load_memory()

    return memory.get(key)


NAME_FILE = "user.txt"


def load_name():

    if os.path.exists(NAME_FILE):
        with open(NAME_FILE, "r") as file:
            name = file.read().strip()
            return name if name else None

    return None


def save_name(name):

    with open(NAME_FILE, "w") as file:
        file.write(name.strip())
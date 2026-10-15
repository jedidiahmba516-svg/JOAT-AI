import json
import os
from difflib import SequenceMatcher

FILE_NAME = "knowledge.json"


def load_knowledge():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_knowledge(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def normalize(text):
    return " ".join((text or "").lower().strip().split())


def learn(question, answer):
    knowledge = load_knowledge()
    knowledge[normalize(question)] = answer.strip()
    save_knowledge(knowledge)


def search(question):
    key = normalize(question)
    if not key:
        return None

    knowledge = load_knowledge()
    if key in knowledge:
        return knowledge[key]

    # Small fuzzy layer for typos / slightly different wording.
    best_key = None
    best_score = 0.0
    for saved_key in knowledge:
        score = SequenceMatcher(None, key, saved_key).ratio()
        if score > best_score:
            best_key, best_score = saved_key, score

    if best_key and best_score >= 0.88:
        return knowledge[best_key]

    return None

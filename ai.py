from config import PERSONALITY

def ask_ai(message):

    prompt = f"""
{PERSONALITY}

User:
{message}

Genesis:
"""

    return prompt
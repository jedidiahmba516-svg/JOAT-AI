import re
from datetime import datetime


def get_time():

    return datetime.now().strftime("%I:%M %p")


def get_date():

    return datetime.now().strftime("%A, %B %d, %Y")


def calculate(expression):

    try:
        return str(eval(expression))
    except:
        return "Sorry, I couldn't calculate that."



def extract_math(message):

    message = message.lower()

    replacements = {
        "divided by": "/",
        "multiplied by": "*",
        "times": "*",
        "plus": "+",
        "minus": "-",
        "divide": "/",
    }

    for old, new in replacements.items():
        message = message.replace(old, new)

    # only replace x between numbers
    message = re.sub(r"(?<=\d)\s*[x×]\s*(?=\d)", "*", message)

    match = re.search(r"(\d+\s*[\+\-\*/]\s*\d+)", message)

    if match:
        return match.group(1)

    return None
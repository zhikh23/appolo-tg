import re


def validate_url(s: str):
    return re.match(
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}"
        r"\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)", s
    ) is not None

import re

from constants import MIN_RESOURCE_NAME_LENGTH


def validate_url(s: str) -> bool:
    return re.match(
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}"
        r"\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)", s
    ) is not None


def validate_tag(s: str) -> bool:
    return re.match(
        r"^#[а-яА-Яa-zA-Z0-9]+$", s
    ) is not None


def validate_resource_name(s: str) -> bool:
    return len(s) > MIN_RESOURCE_NAME_LENGTH

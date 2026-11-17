import re


# Only collapses whitespace (tabs, newlines, double spaces) into one space.
def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
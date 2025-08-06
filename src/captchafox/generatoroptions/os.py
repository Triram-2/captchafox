import random


def generate_os() -> str:
    "Случайная операционка"
    num = random.random()
    if num < 0.901:
        return "windows"
    elif num < 0.945:
        return "macos"
    else:
        return "linux"

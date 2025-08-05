from browserforge.fingerprints import Screen


def generate_screen() -> Screen:
    num = random.choice()
    if num < 0.3681:
        return Screen(max_width=1920, max_height=1080)
    elif num < 0.5318:
        return Screen(max_width=1536, max_height=864)
    elif num < 0.6837:
        return Screen(max_width=1366, max_height=768)
    elif num < 0.7692:
        return Screen(max_width=1280, max_height=720)
    elif num < 0.8276:
        return Screen(max_width=1440, max_height=900)
    elif num < 0.886:
        return Screen(max_width=2560, max_height=1440)
    elif num < 0.9296:
        return Screen(max_width=800, max_height=600)
    elif num < 0.9648:
        return Screen(max_width=1600, max_height=900)
    else:
        return Screen(max_width=1280, max_height=960)
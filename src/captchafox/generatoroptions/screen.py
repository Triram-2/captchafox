from browserforge.fingerprints import Screen


def generate_screen() -> Screen:
    return Screen(max_width=2560, max_height=1440, min_width=800, min_height=600)

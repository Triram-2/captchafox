import random

from typing import Dict, Any

from camoufox import DefaultAddons

from .os import generate_os
from .screen import generate_screen

from .webgl_config import generate_webgl_config
from .config import generate_config


class GeneratorOptions:
    def __init__(self): ...
    def generate(self, launch_options: Dict[str, Any]) -> Dict[str, Any]:
        # Можно задать пользователю
        launch_options["headless"] = "virtual" if launch_options.get("headless", False) else False
        launch_options["locale"] = launch_options.get(
            "locale", None
        )  # Список локалей-языков, например ["en-US", "fr-FR", "de-DE"]

        # Априори
        launch_options["humanize"] = True
        launch_options["geoip"] = True

        launch_options["block_images"] = False
        launch_options["block_webrtc"] = False
        launch_options["block_webgl"] = False

        # Полностью случайно
        self._exclude_ublock(launch_options)
        launch_options["os"] = generate_os()
        launch_options["screen"] = generate_screen()

        # Случайно, но зависят от заданных значений выше
        launch_options["webgl_config"] = generate_webgl_config(launch_options)
        launch_options["config"] = generate_config(launch_options)

        return launch_options

    @staticmethod
    def _exclude_ublock(launch_options: Dict[str, Any]) -> None:
        if random.random() < 0.6:
            launch_options["exclude_addons"] = [DefaultAddons.UBO]

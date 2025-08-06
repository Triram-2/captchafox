from typing import Any

from camoufox.async_api import AsyncCamoufox

from generatoroptions import GeneratorOptions


generator = GeneratorOptions()


class Captchafox(AsyncCamoufox):
    def __init__(self, **launch_options: Any) -> None:
        if not hasattr(launch_options, "launch_options") or getattr(launch_options, "launch_options", None) == "auto":
            launch_options = generator.generate(launch_options)
        super().__init__(**launch_options)

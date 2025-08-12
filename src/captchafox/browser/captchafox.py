from typing import Any, Optional

from camoufox.async_api import AsyncCamoufox
from playwright.async_api import Browser

from generatoroptions import GeneratorOptions


generator = GeneratorOptions()


class Captchafox(AsyncCamoufox):
    def __init__(self, **launch_options: Any) -> None:
        if not hasattr(launch_options, "launch_options") or getattr(launch_options, "launch_options", None) == "auto":
            launch_options = generator.generate(launch_options)
        super().__init__(**launch_options)
        self._opened: bool = False
        self._handle: Optional[Browser] = None

    async def run(self) -> Browser:
        """Запустить Camoufox без контекстного менеджера."""
        if self._opened:
            # уже запущен; вернуть дескриптор
            assert self._handle is not None
            return self._handle
        # Внутри AsyncCamoufox это делает ровно то же, что `async with ...`
        self._handle = await super().__aenter__()
        self._opened = True
        return self._handle  # type: ignore[reportReturnType]

    async def close(self) -> None:
        """Корректно закрыть всё, как при выходе из `async with`."""
        if not self._opened:
            return
        await super().__aexit__(None, None, None)
        self._opened = False
        self._handle = None

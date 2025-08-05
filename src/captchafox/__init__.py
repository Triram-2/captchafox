import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "captchafox"
sys.path.insert(0, str(root))


from browser import Captchafox
from fingerprints import GeneratorOptions


__all__ = ["Captchafox", "__version__", "GeneratorOptions"]

__version__: str = "0.8.0"

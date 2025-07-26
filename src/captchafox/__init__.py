import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "captchafox"
sys.path.insert(0, str(root))


from browser import Captchafox


__all__ = ["Captchafox", "__version__"]

__version__: str = "0.7.0"

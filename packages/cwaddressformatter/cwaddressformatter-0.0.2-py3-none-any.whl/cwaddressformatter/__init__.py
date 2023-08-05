from . import version
from . import main

__version__ = version.VERSION

getAddress = main.getAddress

__all__ = ["__version__", "getAddress"]

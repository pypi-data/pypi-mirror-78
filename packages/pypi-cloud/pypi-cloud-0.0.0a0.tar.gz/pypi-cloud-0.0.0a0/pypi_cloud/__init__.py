"""Host a personal PyPi clone in the cloud."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"  # package is not installed

"""Top-level package for NiFi's FlowFile Format."""
from ._version import version as __version__  # noqa: F401
from .stream import open
from .flowfile import FlowFile

__all__ = ["open", "FlowFile"]

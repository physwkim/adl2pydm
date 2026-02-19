"""Convert MEDM's .adl files to PyDM's .ui format."""

__project__ = "adl2pydm"
__url__ = "https://github.com/physwkim/adl2pydm"

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0+unknown"

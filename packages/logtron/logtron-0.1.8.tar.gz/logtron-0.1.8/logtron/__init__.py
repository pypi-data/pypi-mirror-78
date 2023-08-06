from importlib_metadata import version
from logtron.autodiscover import autodiscover

try:
    __version__ = version(__package__)
except:
    pass

from .config import (
    __all__ as config_all,
    Configuration, Logger_configuration, Env_vars )
from .logger import *  # noqa
from chibi.file import Chibi_path


__all__ = config_all + logger.__all__


configuration = Configuration(
    loggers=Logger_configuration(),
    env_vars=Env_vars(),
)


def default_file_load():
    config_home = configuration.env_vars.HOME
    if not config_home:
        return

    config_home = Chibi_path( configuration.env_vars.XDG_CONFIG_HOME )
    if not config_home:
        config_home = Chibi_path( '~/.config' )

    config_home += 'chibi'
    if not config_home.exists:
        config_home.mkdir()

    config_file = config_home + 'chibi.py'
    if not config_file.exists:
        config_file.touch()
    load( config_file )


def load( path ):
    configuration.load( path )


default_file_load()

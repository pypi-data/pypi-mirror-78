import logging


__all__ = [ 'basic_config', 'silent' ]


def basic_config( level=logging.INFO ):
    from . import configuration
    if configuration.env_vars.PYTHON_UNITTEST_LOGGER:
        level = configuration.env_vars.PYTHON_UNITTEST_LOGGER
    logger_formarter = '%(levelname)s %(name)s %(asctime)s %(message)s'
    logging.basicConfig( level=level, format=logger_formarter )


def silent():
    basic_config( logging.ERROR )

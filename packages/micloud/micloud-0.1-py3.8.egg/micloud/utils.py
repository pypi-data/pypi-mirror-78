import logging
import config
from lazyme.string import color_print


def log_msg(msg, color='gray', level=logging.INFO, offset=False, bold=False):
    if offset:
        msg = '      ' + msg
    
    if level == logging.DEBUG and config.DEBUG:
        config.LOGGER.debug(msg)
    elif level == logging.INFO:
        config.LOGGER.info(msg)
    elif level == logging.WARN or level == logging.WARNING:
        config.LOGGER.warning(msg)
        if color == 'gray':
            color = 'yellow'
    elif level == logging.ERROR:
        config.LOGGER.error(msg)
        if color == 'gray':
            color = 'red'
    elif level == logging.CRITICAL:
        config.LOGGER.critical(msg)
        if color == 'gray':
            color = 'red'

    if (level == logging.DEBUG) and (not config.DEBUG):
        return
    
    color_print(msg, color=color, bold=bold)
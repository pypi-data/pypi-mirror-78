
import logging
import os
import configparser


def load(project):
    config = _get_options()

    if config is None:
        return

    return config


def _get_options():

    hf = os.path.abspath(os.path.expanduser("~") + "/.gspm")

    logging.debug('- looking for options file [.gspm] in User folder [{0}]'.format(hf))

    if os.path.exists(hf):
        logging.debug('- found it')
        config = configparser.ConfigParser()
        config.read(hf)
        return config

    return

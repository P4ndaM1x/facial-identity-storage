import configparser

from .Logger import *


def initConfig(config_filepath):
    logger = initLogger()
    logger.debug("Loading configuration file")
    configParser = configparser.RawConfigParser()
    configParser.read(config_filepath)

    return configParser

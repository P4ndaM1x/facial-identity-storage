import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[30;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"

    reset = "\x1b[0m"
    format = "%(levelname)-8s | %(filename)s:%(lineno)d | %(message)s"
    suffix = format + reset

    FORMATS = {
        logging.DEBUG: grey + suffix,
        logging.INFO: blue + suffix,
        logging.WARNING: yellow + suffix,
        logging.ERROR: red + suffix,
        logging.CRITICAL: bold_red + suffix,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def initLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)

    return logger

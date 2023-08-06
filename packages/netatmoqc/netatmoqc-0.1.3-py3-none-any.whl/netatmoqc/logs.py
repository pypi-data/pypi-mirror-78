import logging


class CustomFormatter(logging.Formatter):
    """
    Logging Formatter to add colors and count warning / errors

    Adapted from: <https://stackoverflow.com/questions/14844970/modifying-
        logging-message-format-based-on-message-logging-level-in-python3>
    """

    reset = "\u001b[0m"
    yellow = "\u001b[33m"
    red = "\u001b[31m"
    green = "\u001b[32m"

    FORMATS = {
        "DEFAULT": "%(asctime)s: %(message)s",
        logging.CRITICAL: (
            red
            + "%(asctime)s %(levelname)s(%(module)s: %(lineno)d): %(message)s"
            + reset
        ),
        logging.ERROR: red
        + "%(asctime)s %(levelname)s: "
        + reset
        + "%(message)s",
        logging.WARNING: yellow
        + "%(asctime)s %(levelname)s: "
        + reset
        + "%(message)s",
        logging.DEBUG: (
            green
            + "%(asctime)s %(levelname)s(%(module)s: %(lineno)d): "
            + reset
            + "%(message)s"
        ),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger(name, loglevel):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler()
    logger_handler.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=logging.getLevelName(loglevel.upper()),
        handlers=[logger_handler],
    )
    return logger

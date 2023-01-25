import logging
import sys

did_init = False


def init_logging(log_file="log.log"):
    global did_init
    if did_init:
        return

    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format='%(asctime)s [%(name)s] <%(levelname)s> %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # SUPPRESS USELESS SELENIUM MESSAGES
    logger = logging.getLogger('urllib3.connectionpool')
    logger.setLevel(logging.INFO)

    logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    logger.setLevel(logging.WARNING)

    did_init = True

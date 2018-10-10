import logging


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler('log.log', mode='w')
    fh.setLevel(logging.INFO)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s - %(name)15s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(name)25s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

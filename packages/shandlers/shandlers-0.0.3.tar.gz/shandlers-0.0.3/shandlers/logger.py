import logging

FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"

logging.basicConfig(format=FORMAT)


def create_logger():
    logger_instance = logging.getLogger()
    logger_instance.setLevel(logging.INFO)
    return logger_instance

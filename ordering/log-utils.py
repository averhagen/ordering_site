import logging
import datetime

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def logged_function(func):
    def wrapper(*args, **kwargs):
        logging.debug(func.__name__ + " START")
        logging.debug(datetime.datetime.now())
        result = func(*args, **kwargs)
        logging.debug(datetime.datetime.now())
        logging.debug(func.__name__ + " END\n")
        return result
    return wrapper

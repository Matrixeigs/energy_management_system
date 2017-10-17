"""
Information logging package imported from LongQi' work
"""
import logging
from os import mkdir
from time import time

# check log folder, create one if it not exist
try:
    mkdir('log')
except FileExistsError:
    pass

apslogger = logging.getLogger('apscheduler')
apslogger.propagate = False
apslogger.setLevel(logging.WARNING)
apshandler = logging.FileHandler('log/apslogger.log')  # as per what you want
apslogger.addHandler(apshandler)


def construct_msg(func):
    def inner(self, msg):
        # new_msg = self.name # this also works, the decorator can access class member
        new_msg = ''
        if isinstance(msg, tuple):
            for m in msg:
                m = m if isinstance(m, str) else str(m)
                new_msg = new_msg + m + ' '
        else:
            new_msg = msg
        func(self, new_msg)

    return inner


class Logger():
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger('EMS.' + self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        fh = logging.FileHandler('log/' + self.name + '.log')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(logging.Formatter('%(asctime)s; %(name)s - %(message)s'))

        self.colors = {'pink': '\033[95m',
                       'blue': '\033[94m',
                       'green': '\033[92m',
                       'yellow': '\033[93m',
                       'red': '\033[91m',
                       'ENDC': '\033[0m',
                       'bold': '\033[1m',
                       'underline': '\033[4m'}

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(
            logging.Formatter(
                self.str_color('green', '%(asctime)s ') +
                self.str_color('blue', '%(name)s ') +
                self.str_color('yellow', '%(message)s')))

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def str_color(self, color, data):
        return self.colors[color] + str(data) + self.colors['ENDC']

    @construct_msg
    def error(self, msg):
        self.logger.error(self.str_color('red', msg))

    @construct_msg
    def warning(self, msg):
        self.logger.warning(self.str_color('yellow', msg))

    @construct_msg
    def info(self, msg):
        self.logger.info(self.str_color('pink', msg))

    @construct_msg
    def debug(self, msg):
        self.logger.debug(self.str_color('green', msg))


def one_min_timestamp():
    """
    get the most closest 1 min timestamp in seconds
    :return:
    """
    curr = round(time())
    return curr - curr % 60


def five_min_timestamp():
    """
    get the most closest 5 mins timestamp in seconds
    :return:
    """
    curr = round(time())
    return curr - curr % 300


def one_hour_timestamp():
    """
        get the most closest one hour timestamp in seconds
        :return:
        """
    curr = round(time())
    return curr - curr % 3600


if __name__ == "__main__":
    log = Logger('test')
    log.info('info: say something.')
    log.debug(('info: say something. ', 'comes from a tuple ', 54545))
    print(one_hour_timestamp())

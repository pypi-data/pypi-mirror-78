from enum import Enum

DEBUG    = True
SIMULATE = True
TOKEN   = '7GCHhzdd2iJF2jBLWbkxjfHV'
LOGGER   = None
NAME     = ''
TEST_COLOR = 'red'

class Flag(Enum):
    UNKNOWN = 0
    QUIT    = 1
    CMD     = 2
    SUCCESS = 3
    ERROR   = 4

from enum import Enum


class Privilege(Enum):
    READ = 'READ'
    WRITE = 'WRITE'
    ALL = 'ALL'

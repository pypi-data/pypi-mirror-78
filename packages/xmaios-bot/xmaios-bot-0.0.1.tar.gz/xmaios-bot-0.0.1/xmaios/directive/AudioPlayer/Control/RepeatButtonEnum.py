#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from enum import Enum, unique

@unique
class RepeatButtonEnum(Enum):
    REPEAT_ONE = 'REPEAT_ONE'
    REPEAT_ALL = 'REPEAT_ALL'
    REPEAT_SHUFFLE = 'SHUFFLE'

    @staticmethod
    def inEnum(repeatButton):
        return repeatButton in RepeatButtonEnum.__members__.values()

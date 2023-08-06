#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from enum import Enum, unique


@unique
class TextContentPosition(Enum):
    TOP_LEFT = 'TOP-LEFT'
    CENTER = 'CENTER'
    BOTTOM_LEFT = 'BOTTOM-LEFT'

    @staticmethod
    def inEnum(position):

        return position in TextContentPosition.__members__.values()

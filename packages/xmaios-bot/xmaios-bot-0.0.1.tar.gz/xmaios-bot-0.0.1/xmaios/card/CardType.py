#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from enum import Enum

"""
    desc:pass
"""


class CardType(Enum):
    CARD_TYPE_IMAGE = 'image'
    CARD_TYPE_CUSTOM_SERVICE = 'custom_service'
    CARD_TYPE_FUNC = 'func'  # 猜你想要功能模板
    CARD_TYPE_TXT = 'txt'
    CARD_TYPE_WEB = 'web'




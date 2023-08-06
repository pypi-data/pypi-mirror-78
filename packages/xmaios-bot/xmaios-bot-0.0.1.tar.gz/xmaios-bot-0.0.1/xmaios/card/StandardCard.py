#!/usr/bin/env python3
# -*- encoding=utf-8 -*-



from xmaios.card.BaseCard import BaseCard
import xmaios.card.CardType as CardType


class StandardCard(BaseCard):
    """
    标准卡片
    详见文档：https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-custom/cards_markdown#%E6%A0%87%E5%87%86%E5%8D%A1%E7%89%87
    """

    def __init__(self):
        super(StandardCard, self).__init__(['title', 'content', 'image'])
        self.data['type'] = CardType.CARD_TYPE_STANDARD


if __name__ == '__main__':
    pass

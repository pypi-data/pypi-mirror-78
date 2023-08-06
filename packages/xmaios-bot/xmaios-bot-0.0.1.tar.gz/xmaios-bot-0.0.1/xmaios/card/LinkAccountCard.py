#!/usr/bin/env python3
# -*- encoding=utf-8 -*-



from xmaios.card.BaseCard import BaseCard
import xmaios.card.CardType as CardType


class LinkAccountCard(BaseCard):
    """
    第三方账号授权
    debug模式：要将回调地址域名替换下 https://xiaodu-dbp.baidu.com/xxxx
    """

    def __init__(self):
        BaseCard.__init__(self)
        self.data['type'] = CardType.CARD_TYPE_LINKACCOUNT


if __name__ == '__main__':
    pass
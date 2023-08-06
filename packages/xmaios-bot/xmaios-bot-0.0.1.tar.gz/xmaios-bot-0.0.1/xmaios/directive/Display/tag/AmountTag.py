#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class AmountTag(BaseTag):

    def __init__(self, amount):
        super(AmountTag, self).__init__(TagTypeEnum.TAG_TYPE_AMOUNT, amount)
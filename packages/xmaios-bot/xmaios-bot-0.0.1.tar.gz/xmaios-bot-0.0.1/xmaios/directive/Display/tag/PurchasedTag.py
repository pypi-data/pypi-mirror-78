#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum
from xmaios.directive.Display.tag.BaseTag import BaseTag


class PurchasedTag(BaseTag):

    def __init__(self):
        super(PurchasedTag, self).__init__(TagTypeEnum.TAG_TYPE_PURCHASED, '已购')

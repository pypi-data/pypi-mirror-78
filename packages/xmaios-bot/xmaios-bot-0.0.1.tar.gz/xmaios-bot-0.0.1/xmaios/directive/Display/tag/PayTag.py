#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class PayTag(BaseTag):

    def __init__(self):
        super(PayTag, self).__init__(TagTypeEnum.TAG_TYPE_PAY, '付费')

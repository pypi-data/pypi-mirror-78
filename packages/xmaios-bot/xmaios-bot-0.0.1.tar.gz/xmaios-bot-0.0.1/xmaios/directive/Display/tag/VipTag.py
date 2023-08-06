#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class VipTag(BaseTag):

    def __init__(self):
        super(VipTag, self).__init__(TagTypeEnum.TAG_TYPE_VIP, 'VIP')
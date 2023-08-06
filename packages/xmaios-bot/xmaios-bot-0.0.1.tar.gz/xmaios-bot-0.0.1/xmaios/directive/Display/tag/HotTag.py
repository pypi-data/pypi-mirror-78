#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum
from xmaios.directive.Display.tag.BaseTag import BaseTag


class HotTag(BaseTag):

    def __init__(self):
        super(HotTag, self).__init__(TagTypeEnum.TAG_TYPE_HOT, '热门')

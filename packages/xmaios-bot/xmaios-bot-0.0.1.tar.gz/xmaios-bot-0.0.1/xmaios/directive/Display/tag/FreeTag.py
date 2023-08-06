#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class FreeTag(BaseTag):

    def __init__(self):
        super(FreeTag, self).__init__(TagTypeEnum.TAG_TYPE_FREE, '免费')

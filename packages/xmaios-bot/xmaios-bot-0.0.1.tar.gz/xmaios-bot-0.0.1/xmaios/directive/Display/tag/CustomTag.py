#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class CustomTag(BaseTag):

    def __init__(self, text):
        super(CustomTag, self).__init__(TagTypeEnum.TAG_TYPE_CUSTOM, text)

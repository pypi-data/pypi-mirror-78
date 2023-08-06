#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum
from xmaios.directive.Display.tag.BaseTag import BaseTag


class NewTag(BaseTag):

    def __init__(self):
        super(NewTag, self).__init__(TagTypeEnum.TAG_TYPE_NEW, '最新')
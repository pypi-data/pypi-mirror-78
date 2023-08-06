#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.tag.BaseTag import BaseTag
from xmaios.directive.Display.tag.TagTypeEnum import TagTypeEnum


class TimeTag(BaseTag):

    def __init__(self, time):
        super(TimeTag, self).__init__(TagTypeEnum.TAG_TYPE_TIME, time)

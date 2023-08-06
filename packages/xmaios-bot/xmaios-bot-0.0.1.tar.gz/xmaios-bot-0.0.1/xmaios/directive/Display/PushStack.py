#!/usr/bin/env python3
# -*- encoding=utf-8 -*-



from xmaios.directive.BaseDirective import BaseDirective


class PushStack(BaseDirective):
    """
        用于生成PushStack指令的类
    """

    def __init__(self):
        super(PushStack, self).__init__('Display.PushStack')
#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.DPL.Commands.BaseCommand import BaseCommand


class ScrollCommand(BaseCommand):
    """
    ScrollCommand 窗口滚动指令

    """

    def __init__(self):
        super(ScrollCommand, self).__init__('Scroll')

    def set_distance(self, distance):
        """
        设置滚动的距离
        :param distance: 滚动的距离
        :return:
        """

        if isinstance(distance, str):
            self.data['distance'] = distance

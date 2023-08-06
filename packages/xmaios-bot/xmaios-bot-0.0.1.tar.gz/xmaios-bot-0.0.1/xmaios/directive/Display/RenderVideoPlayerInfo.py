#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.BaseRenderPlayerInfo import BaseRenderPlayerInfo


class RenderVideoPlayerInfo(BaseRenderPlayerInfo):

    def __init__(self, content=None, controls=[]):
        super(RenderVideoPlayerInfo, self).__init__('Display.RenderVideoPlayerInfo', content, controls)
#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.BaseRenderPlayerInfo import BaseRenderPlayerInfo


class RenderAudioPlayerInfo(BaseRenderPlayerInfo):

    def __init__(self, content=None, controls=[]):
        super(RenderAudioPlayerInfo, self).__init__('Display.RenderAudioPlayerInfo', content, controls)
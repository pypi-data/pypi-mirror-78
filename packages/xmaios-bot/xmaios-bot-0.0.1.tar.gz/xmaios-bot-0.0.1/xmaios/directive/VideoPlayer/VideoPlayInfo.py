#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Base.TraitPlayerInfo import TraitPlayerInfo


class VideoPlayInfo(TraitPlayerInfo):

    def __init__(self, content, controls=[]):
        super(VideoPlayInfo, self).__init__()
        self.set_content(content)
        self.set_controls(controls)

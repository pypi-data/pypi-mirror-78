#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.AudioPlayer.PlayerInfo import PlayerInfo


class AudioPlayerInfo(PlayerInfo):

    def __init__(self, content, controls=[]):
        super(AudioPlayerInfo, self).__init__(content, controls)
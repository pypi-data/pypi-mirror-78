#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.AudioPlayer.Control.Button import Button


class PlayPauseButton(Button):

    def __init__(self):
        super(PlayPauseButton, self).__init__('PLAY_PAUSE')

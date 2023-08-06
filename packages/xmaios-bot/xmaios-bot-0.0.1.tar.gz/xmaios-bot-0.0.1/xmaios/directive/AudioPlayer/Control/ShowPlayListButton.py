#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.AudioPlayer.Control.Button import Button


class ShowPlayListButton(Button):

    def __init__(self):
        super(ShowPlayListButton, self).__init__('SHOW_PLAYLIST')

#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.AudioPlayer.Control.BaseButton import BaseButton


class Button(BaseButton):

    def __init__(self, name):
        super(Button, self).__init__('BUTTON', name)
        self.data['enabled'] = True
        self.data['selected'] = False

    def set_enabled(self, enabled):

        self.data['enabled'] = enabled

    def set_selected(self, selected):

        self.data['selected'] = selected

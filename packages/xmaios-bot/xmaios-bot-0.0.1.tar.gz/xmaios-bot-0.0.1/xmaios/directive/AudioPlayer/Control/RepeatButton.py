#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.AudioPlayer.Control.RadioButton import RadioButton
from xmaios.directive.AudioPlayer.Control.RepeatButtonEnum import RepeatButtonEnum


class RepeatButton(RadioButton):

    def __init__(self, selected_value=RepeatButtonEnum.REPEAT_ONE.value):
        super(RepeatButton, self).__init__('REPEAT', selected_value)

    def set_selected_value(self, selected_value=RepeatButtonEnum.REPEAT_ONE):

        if RepeatButtonEnum.inEnum(selected_value):
            self.data['selectedValue'] = selected_value.value
        else:
            self.data['selectedValue'] = RepeatButtonEnum.REPEAT_ONE.value

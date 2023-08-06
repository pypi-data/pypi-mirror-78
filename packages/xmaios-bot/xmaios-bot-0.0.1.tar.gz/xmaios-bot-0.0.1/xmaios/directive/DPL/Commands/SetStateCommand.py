#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.DPL.Commands.BaseCommand import BaseCommand


class SetStateCommand(BaseCommand):

    def __init__(self):
        super(SetStateCommand, self).__init__('SetState')

    def set_state(self, state):
        if state:
            self.data['state'] = state

    def set_value(self, value):

        if value:
            self.data['value'] = value

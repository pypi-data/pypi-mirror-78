#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.DPL.Commands.BaseCommand import BaseCommand


class SendEventCommand(BaseCommand):
    """
    SendEventCommand 绑定端触发UserEvent指令
    """

    def __init__(self):
        super(SendEventCommand, self).__init__('SendEvent')

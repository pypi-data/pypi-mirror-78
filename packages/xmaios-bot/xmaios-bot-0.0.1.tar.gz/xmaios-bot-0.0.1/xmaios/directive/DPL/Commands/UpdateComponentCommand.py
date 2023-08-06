#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.DPL.Commands.BaseCommand import BaseCommand
from xmaios.directive.DPL.Document import Document


class UpdateComponentCommand(BaseCommand):
    """
    异步更新指令
    example:
        updateComponentCommand = UpdateComponentCommand()
        updateComponentCommand.set_component_id("componentId");
        updateComponentCommand.set_document({...});
    """

    def __init__(self):
        super(UpdateComponentCommand, self).__init__('UpdateComponent')

    def set_document(self, document):
        """
        设置替换文档
        :param document:
        :return:
        """

        if isinstance(document, Document):
            self.data['document'] = document.get_data()

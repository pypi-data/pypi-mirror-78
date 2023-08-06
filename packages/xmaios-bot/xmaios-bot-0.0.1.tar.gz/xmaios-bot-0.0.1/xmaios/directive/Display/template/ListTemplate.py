#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.Display.template.BaseTemplate import BaseTemplate
from xmaios.directive.Display.template.ListTemplateItem import ListTemplateItem


class ListTemplate(BaseTemplate):

    def __init__(self, type):
        super(ListTemplate, self).__init__(['token', 'title', 'type'])
        self.set_type(type)
        self.data['listItems'] = []

    def add_item(self, item):
        if isinstance(item, ListTemplateItem):
            self.data['listItems'].append(item.get_data())
        return self

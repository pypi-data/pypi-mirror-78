#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.BaseDirective import BaseDirective


class Hint(BaseDirective):

    def __init__(self, text):
        super(Hint, self).__init__('Hint')
        self.data['hints'] = []
        if type(text) == str:
            text = [text]

        if type(text) == list:
            for value in text:
                item = {'type': 'PlainText', 'text': value}
                self.data['hints'].append(item)
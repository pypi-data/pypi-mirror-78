#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


"""
    desc:pass
"""
from xmaios.directive.BaseDirective import BaseDirective


class RecordSpeech(BaseDirective):

    def __init__(self):
        super(RecordSpeech, self).__init__('Record.RecordSpeech')
        self.data['token'] = self.gen_token()

    def set_token(self, token):
        if token and isinstance(token, str):
            self.data['token'] = token


if __name__ == '__main__':
    pass

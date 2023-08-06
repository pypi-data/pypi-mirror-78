#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.BaseDirective import BaseDirective
from xmaios.directive.Base.TraitPlayerInfo import TraitPlayerInfo


class BaseRenderPlayerInfo(TraitPlayerInfo, BaseDirective):

    def __init__(self, directive_type, content, controls=[]):
        super(BaseRenderPlayerInfo, self).__init__()
        BaseDirective.__init__(self, directive_type)
        self.data['token'] = self.gen_token()
        self.set_content(content)
        self.set_controls(controls)

    def set_token(self, token):
        if token:
            self.data['token'] = token


if __name__ == '__main__':
    pass
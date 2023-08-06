#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.directive.BaseDirective import BaseDirective
from xmaios.directive.DPL.Document import Document


class RenderDocument(BaseDirective):

    def __init__(self):
        super(RenderDocument, self).__init__('DPL.RenderDocument')
        self.data['token'] = self.gen_token()

    def set_document(self, document):
        if isinstance(document, Document):
            self.data['document'] = document.get_data()

    def set_data_source(self, data_source):
        if data_source:
            self.data['dataSources'] = data_source
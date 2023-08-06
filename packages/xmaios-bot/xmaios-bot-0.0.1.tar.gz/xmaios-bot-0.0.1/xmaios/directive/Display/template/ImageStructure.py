#!/usr/bin/env python3
# -*- encoding=utf-8 -*-



class ImageStructure(object):

    def __init__(self):
        self.data = {}
        super(ImageStructure, self).__init__()

    def set_url(self, url):
        if url:
            self.data['url'] = url

    def set_width_pixels(self, width):
        if width:
            self.data['widthPixels'] = width

    def set_height_pixels(self, height):
        if height:
            self.data['heightPixels'] = height

    def get_data(self):
        return self.data

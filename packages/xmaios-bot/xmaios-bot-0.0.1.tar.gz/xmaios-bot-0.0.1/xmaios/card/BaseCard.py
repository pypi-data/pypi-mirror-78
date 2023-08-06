#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from xmaios.Request import Request
from enum import Enum
"""
卡片基类
"""


class View(object):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data


class Speaker(Enum):
    WENXI = 'wenxi'
    DEFAULT = 'nana'


class TTSData(object):

    def __init__(self, text='', speaker=None, speed=None, volume=None, pitch=None):
        """

        :param text: 待合成文本
        :param speaker: 来源，默认为default，文章播报为wenxi
        :param speed: 速度
        :param volume: 音量
        :param pitch: 音调
        """
        self.text = text
        self.speaker = speaker
        self.speed = speed
        self.volume = volume
        self.pitch = pitch

    @property
    def data(self) -> dict:
        _data = {"Text": self.text}
        if self.speaker:
            _data['Speaker'] = self.speaker
        if self.speed:
            _data['Speed'] = self.speed
        if self.volume:
            _data['Volume'] = self.volume
        if self.pitch:
            _data['Pitch'] = self.pitch
        return _data


class CapsuleItemData(object):

    def __init__(self, text, action='SendText'):
        self._text = text
        self._action = action
        assert self._action in ('SendText',)

    @property
    def text(self):
        return self._text

    @property
    def action(self):
        return self._action


class CapsuleView(View):
    def __init__(self, font='12', color='#FFFFFF', opacity='0.5', spacing='8',
                 background_color='#FFFFFF', background_opacity='0.0', border_color='#FFFFFF',
                 padding_top_bottom="5", padding_left_right="15",
                 border_radius='14', border_opacity='0.3', border_width='0.5', margin_left='15', items=None):
        assert items and isinstance(items, list)
        items_data = [{'Text': x.text, 'Action': x.action} for x in items if isinstance(x, CapsuleItemData)]
        assert items_data
        data = {"Font": font, "Color": color, "Opacity": opacity, "Spacing": spacing,
                "BackgroundColor": background_color, "BackgroundOpacity": background_opacity,
                "BorderColor": border_color,
                "BorderOpacity": border_opacity, "BorderWidth": border_width, "PaddingLeftRight": padding_left_right,
                "PaddingTopBottom": padding_top_bottom, "MarginLeft": margin_left,
                "BorderRadius": border_radius, "Items": items_data}
        super().__init__(data)


class BaseCard(object):

    def __init__(self, request_data):
        # 用户说
        self._request_data = request_data
        self._user_text = ''
        # 客户端版本
        self._client_version = ''
        # 设备类型 android/ios
        self._device_type = ''

        # 返回数据
        self.data = {}

        self._parse_request_data()

    def _parse_request_data(self):
        if 'request' in self._request_data:
            bot_request = Request(self._request_data)
            self._user_text = bot_request.text if bot_request.text else ''
            self._device_type = bot_request.device_type if bot_request.device_type else ''
            self._client_version = bot_request.client_version if bot_request.client_version else ''
        else:
            if 'user_text' in self._request_data:
                self._user_text = self._request_data['user_text']
            if 'client_version' in self._request_data:
                self._client_version = self._request_data['client_version']
            if 'device_type' in self._request_data:
                self._device_type = self._request_data['device_type']

    @property
    def type(self):
        return self.data['type']

    @property
    def user_text(self):
        return self._user_text

    @property
    def client_version(self):
        return self._client_version

    @property
    def device_type(self):
        return self._device_type

    def get_data(self):
        # ios 8.3模板约定必须含有此字段
        assert 'Background' in self.data['TemplateData']['Template'], 'Template Background null'
        return self.data

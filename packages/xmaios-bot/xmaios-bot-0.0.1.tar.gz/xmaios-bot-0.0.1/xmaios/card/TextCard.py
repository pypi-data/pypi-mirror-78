#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from xmaios.card.BaseCard import BaseCard, CapsuleView, TTSData
from xmaios.card.CardType import CardType
import copy

template_data = {
    "Template": {
        "TemplateName": "PureText",
        "VoiceContent": "",
        "Background": {"Color": "#FFFFFF", "Opacity": "0.05", "BorderRadius": "4", "MarginLeft": "15",
                       "MarginRight": "15", "Padding": "15"},
        "Request": {"Text": "", "Font": "22", "Color": "#FFFFFF", "Opacity": "0.5", "LineHeight": "30"},
        "Response": {"Text": "", "Font": "22", "Color": "#FFFFFF", "Opacity": "1.0",
                     "LineHeight": "30"},
    },
    "Control": {"DirectJump": "false", "Url": ""}
}


class TextCard(BaseCard):
    """
    文本卡片
    """

    def __init__(self, request_data: dict, content: str = None, direct_jump: str = 'false',
                 jump_url: str = None, voice_content: str = None, show_background: bool = True,
                 background_color='#FFFFFF', background_opacity='0.05', border_radius='4',
                 margin_left='15', margin_right='15', padding='15',
                 capsule_view: CapsuleView = None,
                 tts_data: TTSData = None):
        """
        文本卡片显示的content
        :param content:
        """
        super(TextCard, self).__init__(request_data)
        self.data['type'] = CardType.CARD_TYPE_TXT.value
        self._content = content
        self._direct_jump = direct_jump
        self._jump_url = jump_url
        self._show_background = show_background
        self._direct_jump_hint = '已经找到，即将为您跳转'
        self._voice_content = voice_content
        self._capsule_view = capsule_view
        self._background_color = background_color
        self._background_opacity = background_opacity
        self._border_radius = border_radius
        self._margin_left = margin_left
        self._margin_right = margin_right
        self._padding = padding
        self._tts_data = tts_data
        self._render()

    def _render(self):
        _template = copy.deepcopy(template_data)
        _template['Template']['Request']['Text'] = self.user_text
        _template['Control']['Url'] = self._jump_url
        if self._content is not None:
            _template['Template']['Response']['Text'] = self._content
        else:
            _template['Template']['Response']['Text'] = self._direct_jump_hint
        if self._voice_content is not None:
            _template['Template']['VoiceContent'] = self._voice_content
        else:
            _template['Template']['VoiceContent'] = _template['Template']['Response']['Text']

        if not self._show_background:
            _template['Template']['Background']['Opacity'] = '0.0'

        if isinstance(self._background_color, str):
            _template['Template']['Background']['Color'] = self._background_color
        if isinstance(self._background_opacity, str):
            _template['Template']['Background']['Opacity'] = self._background_opacity
        if isinstance(self._border_radius, str):
            _template['Template']['Background']['BorderRadius'] = self._border_radius
        if isinstance(self._margin_left, str):
            _template['Template']['Background']['MarginLeft'] = self._margin_left
        if isinstance(self._margin_right, str):
            _template['Template']['Background']['MarginRight'] = self._margin_right
        if isinstance(self._padding, str):
            _template['Template']['Background']['Padding'] = self._padding

        if self._direct_jump:
            _template['Control']['DirectJump'] = self._direct_jump
        if self._jump_url:
            _template['Control']['Url'] = self._jump_url
        if self._capsule_view:
            _template['Capsule'] = self._capsule_view.data
        if self._tts_data and self._tts_data.text:
            _template['TTS'] = self._tts_data.data

        self.data['TemplateData'] = _template

    def set_font_size(self, size: int):
        self.data['TemplateData']['Template']['Response']['Font'] = str(size)

    def set_font_color(self, color: str):
        self.data['TemplateData']['Template']['Response']['Color'] = color

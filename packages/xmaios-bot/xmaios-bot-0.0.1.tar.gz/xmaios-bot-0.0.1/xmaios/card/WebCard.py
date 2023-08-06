#!/usr/bin/env python
# encoding: utf-8

from xmaios.card.BaseCard import BaseCard, CapsuleView, TTSData
from xmaios.card.CardType import CardType
import copy
import base64

template_data = {
    "Template": {
        "TemplateName": "WebAnswer",
        "VoiceContent": "",
        "WebDecode": "false",
        "WebTransparent": "false",
        "CssFileName": "RemoteFAQ.css",
        "JsFileName": "RemoteFAQ.js",
        "Background": {"Color": "#FFFFFF", "Opacity": "0.05", "BorderRadius": "4", "MarginLeft": "15",
                       "MarginRight": "15", "Padding": "15"},
        "Request": {"Text": "", "Font": "22", "Color": "#FFFFFF", "Opacity": "0.5", "LineHeight": "30"},
        "Response": {"Text": ""},
    },
    "Control": {"DirectJump": "false", "Url": ""}
}


class WebCard(BaseCard):
    """

    """

    def __init__(self, request_data, content, voice_content='', transparent='true',
                 show_background: bool = False,
                 background_margin_left: str = '15',
                 background_margin_right: str = '15',
                 background_padding: str = '15',
                 background_border_radius: str = '4',
                 capsule_view: CapsuleView = None,
                 tts_data: TTSData = None
                 ):
        """
        文本卡片显示的content
        :param content:
        """
        super(WebCard, self).__init__(request_data)
        self.data['type'] = CardType.CARD_TYPE_WEB.value
        self._content = content
        self._voice_content = voice_content
        self._transparent = transparent
        self._show_background = show_background
        self._background_margin_left = background_margin_left
        self._background_margin_right = background_margin_right
        self._background_padding = background_padding
        self._background_border_radius = background_border_radius
        self._capsule_view = capsule_view
        self._tts_data = tts_data
        self._render()

    def _render(self):
        _template = copy.deepcopy(template_data)
        _template['Template']['Request']['Text'] = self.user_text
        if self.client_version >= '7.5.0':
            _template['Template']['WebDecode'] = 'true'
            _template['Template']['WebTransparent'] = self._transparent
            _template['Template']['Response']['Text'] = \
                base64.b64encode(self._content.encode('utf-8')).decode('utf-8')
        else:
            _template['Template']['Response']['Text'] = self._content

        if not self._show_background:
            _template['Template']['Background']['Opacity'] = '0.0'

        if isinstance(self._background_margin_left, str):
            _template['Template']['Background']['MarginLeft'] = self._background_margin_left

        if isinstance(self._background_margin_right, str):
            _template['Template']['Background']['MarginRight'] = self._background_margin_right

        if isinstance(self._background_padding, str):
            _template['Template']['Background']['Padding'] = self._background_padding

        if isinstance(self._background_border_radius, str):
            _template['Template']['Background']['BorderRadius'] = self._background_border_radius

        # 非透明默认样式处理
        if self.client_version >= '8.3.0' and self._transparent == 'false':
            _template['Template']['Background']['MarginLeft'] = '20'
            _template['Template']['Background']['MarginRight'] = '20'
            _template['Template']['Background']['Opacity'] = '1.0'

        if self._capsule_view:
            _template['Capsule'] = self._capsule_view.data
        # 注意，若此字段下发，则使用此数据播报，而不用VoiceContent字段
        if self._tts_data and self._tts_data.text:
            _template['TTS'] = self._tts_data.data
        _template['Template']['VoiceContent'] = self._voice_content
        self.data['TemplateData'] = _template

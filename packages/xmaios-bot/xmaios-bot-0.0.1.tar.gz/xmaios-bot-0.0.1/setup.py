#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup

setup(
    name='xmaios-bot',
    version='0.0.1',
    author='',
    author_email='',
    description='Third party XmaiOS Bot Python SDK',
    keywords='xmaios bot',
    url='',
    packages=[
        'xmaios.card',
        'xmaios.directive',
        'xmaios.directive.Base',
        'xmaios.directive.AppLauncher',
        'xmaios.directive.AudioPlayer',
        'xmaios.directive.AudioPlayer.Control',
        'xmaios.directive.Display',
        'xmaios.directive.Display.media',
        'xmaios.directive.Display.tag',
        'xmaios.directive.Display.template',
        'xmaios.directive.DPL',
        'xmaios.directive.DPL.Commands',
        'xmaios.directive.Pay',
        'xmaios.directive.Permission',
        'xmaios.directive.Record',
        'xmaios.directive.VideoPlayer',
        'xmaios.directive.WebBrowser',
        'xmaios.monitor',
        'xmaios.monitor.model',
        'xmaios.plugins',
        'xmaios.',
    ],
    platforms='py3',
    install_requires=[
        'requests',
         'pyOpenSSL'
    ]
)

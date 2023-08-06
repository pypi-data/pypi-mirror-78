#!/usr/bin/env python
# encoding: utf-8

from enum import Enum


class ConfirmationStatus(Enum):
    NONE = 'NONE'
    CONFIRMED = 'CONFIRMED'
    DENIED = 'DENIED'


class SysIntentType(Enum):
    HINT_INTENT = 'sys.intent.hint'
    SKIP_INTENT = 'sys.intent.skip'
    RESTART_INTENT = 'sys.intent.restart'
    BEATEN_INTENT = 'sys.intent.beaten'
    NEXT_INTENT = 'sys.intent.next'
    CHOOSE_INTENT = 'sys.intent.choose'
    DENY_INTENT = 'sys.intent.deny'
    CONFIRM_INTENT = 'sys.intent.confirm'
    EXIT_INTENT = 'sys.intent.exit'
    PREVIOUS_INTENT = 'sys.intent.previous'
    PLAY_INTENT = 'sys.intent.play'
    PAUSE_INTENT = 'sys.intent.pause'
    CONTINUE_INTENT = 'sys.intent.continue'
    STOP_INTENT = 'sys.intent.stop'


class DialogDirectiveType(Enum):
    DIALOG_CONFIRM_SLOT = 'Dialog.ConfirmSlot'
    DIALOG_ELICIT_SLOT = 'Dialog.ElicitSlot'
    DIALOG_SELECT_SLOT = 'Dialog.SelectSlot'
    DIALOG_CONFIRM_INTENT = 'Dialog.ConfirmIntent'
    DIALOG_SELECT_INTENT = 'Dialog.SelectIntent'
    DIALOG_DELEGATE = 'Dialog.Delegate'

#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


from xmaios.card.BaseCard import BaseCard


class ListCardItem(BaseCard):

    def __init__(self):
        super(ListCardItem, self).__init__(['title', 'content', 'url', 'image'])


if __name__ == '__main__':
    pass

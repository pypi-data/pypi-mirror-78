# -*- coding: utf-8 -*-

from .channel import Channel


class Version:
    id: int
    name: str
    git_path: str
    channel: Channel

    def __init__(self, obj):
        self.id = obj['id']
        self.name = obj['name']
        self.git_path = obj['gitPath']
        self.channel = Channel(obj['channel'])

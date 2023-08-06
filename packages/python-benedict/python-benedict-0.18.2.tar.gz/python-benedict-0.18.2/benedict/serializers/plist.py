# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import plistlib


class PListSerializer(AbstractSerializer):
    """
    https://docs.python.org/3/library/plistlib.html
    """
    def __init__(self):
        super(PListSerializer, self).__init__()

    def decode(self, s, **kwargs):
        data = plistlib.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = plistlib.dumps(d, **kwargs)
        return data

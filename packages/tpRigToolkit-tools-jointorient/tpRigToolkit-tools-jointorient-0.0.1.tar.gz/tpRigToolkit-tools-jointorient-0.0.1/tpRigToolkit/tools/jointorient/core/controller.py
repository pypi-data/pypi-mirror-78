#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Joint Orient widget controller class implementation
"""

from __future__ import print_function, division, absolute_import


class JointOrientController(object):
    def __init__(self, client, model):
        super(JointOrientController, self).__init__()

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

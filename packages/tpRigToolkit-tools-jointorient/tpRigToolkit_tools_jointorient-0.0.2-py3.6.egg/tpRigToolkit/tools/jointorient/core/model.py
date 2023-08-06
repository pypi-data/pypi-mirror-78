#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Joint Orient widget model class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import *


class JointOrientModel(QObject, object):
    def __init__(self):
        super(JointOrientModel, self).__init__()

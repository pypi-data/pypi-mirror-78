#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains joint utils orient widget implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from functools import partial

from Qt.QtCore import *

import tpDcc as tp
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, buttons


class JointUtilsView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(JointUtilsView, self).__init__(parent=parent)

    def ui(self):
        super(JointUtilsView, self).ui()

        utils_layout = layouts.GridLayout()
        self.main_layout.addLayout(utils_layout)

        self._display_lra_btn = buttons.BaseButton('Display LRA', parent=self)
        self._hide_lra_btn = buttons.BaseButton('Hide LRA', parent=self)
        self._select_hierarchy_btn = buttons.BaseButton('Select Hierarchy', parent=self)

        utils_layout.addWidget(self._display_lra_btn, 0, 0)
        utils_layout.addWidget(self._hide_lra_btn, 0, 1)
        utils_layout.addWidget(self._select_hierarchy_btn, 0, 2)

    def setup_signals(self):
        self._display_lra_btn.clicked.connect(partial(self._controller.set_lra, True))
        self._hide_lra_btn.clicked.connect(partial(self._controller.set_lra, False))
        self._select_hierarchy_btn.clicked.connect(self._controller.select_hierarchy)


class JointUtilsModel(QObject, object):
    def __init__(self):
        super(JointUtilsModel, self).__init__()


class JointUtilsController(object):
    def __init__(self, client, model):
        super(JointUtilsController, self).__init__()

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

    @tp.Dcc.get_repeat_last_decorator(__name__ + '.JointUtilsController')
    def set_lra(self, state):
        return self._client.set_local_rotation_axis(state)

    def select_hierarchy(self):
        return self._client.select_hierarchy()


def joint_utils(client, parent=None):
    model = JointUtilsModel()
    controller = JointUtilsController(client=client, model=model)
    view = JointUtilsView(model=model, controller=controller, parent=parent)

    return view

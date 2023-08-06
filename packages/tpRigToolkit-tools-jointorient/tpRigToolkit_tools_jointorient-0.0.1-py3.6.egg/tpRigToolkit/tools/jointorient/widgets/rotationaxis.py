#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rotation axis orient widget implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from functools import partial
from collections import OrderedDict

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, buttons, combobox, checkbox


class RotationAxisView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(RotationAxisView, self).__init__(parent=parent)

        self.refresh()

    def ui(self):
        super(RotationAxisView, self).ui()

        set_rot_top_layout = layouts.HorizontalLayout(spacing=5)
        self._set_rot_axis_box = combobox.BaseComboBox(parent=self)
        set_rot_top_layout.addWidget(self._set_rot_axis_box)
        for rotAxis in tp.Dcc.ROTATION_AXES:
            self._set_rot_axis_box.addItem(rotAxis)
        set_rot_axis_common_btn = buttons.BaseButton('   <', parent=self)
        set_rot_axis_common_btn.setMaximumWidth(45)
        set_rot_axis_common_btn.setStyleSheet("QPushButton::menu-indicator{image:url(none.jpg);}")
        self._set_rot_axis_common_btn_menu = QMenu(self)
        # self._set_common_rotation_axis()
        set_rot_axis_common_btn.setMenu(self._set_rot_axis_common_btn_menu)
        set_rot_top_layout.addWidget(set_rot_axis_common_btn)

        set_rot_axis_btn_layout = layouts.HorizontalLayout()
        set_rot_axis_btn_layout.setAlignment(Qt.AlignCenter)
        self._set_rot_axis_btn = buttons.BaseButton('Set', parent=self)
        self._affect_children_cbx = checkbox.BaseCheckBox('Affect Children', parent=self)
        self._set_rot_axis_btn.setMaximumWidth(100)
        set_rot_axis_btn_layout.addWidget(self._set_rot_axis_btn)
        set_rot_axis_btn_layout.addWidget(self._affect_children_cbx)

        self.main_layout.addLayout(set_rot_top_layout)
        self.main_layout.addLayout(set_rot_axis_btn_layout)

    def setup_signals(self):
        self._set_rot_axis_box.currentIndexChanged.connect(self._controller.change_rotation_order)
        self._affect_children_cbx.toggled.connect(self._controller.change_affect_children)
        self._set_rot_axis_btn.clicked.connect(self._controller.set_rotation_axis)

        self._model.rotationAxisChanged.connect(self._on_rotation_axis_changed)
        self._model.affectChildrenChanged.connect(self._affect_children_cbx.setChecked)

    def refresh(self):
        self._set_rot_axis_common_btn_menu.clear()

        self._set_rot_axis_box.setCurrentIndex(self._model.rotation_axis)
        self._affect_children_cbx.setChecked(self._model.affect_children)

        available_axises = self._model.available_rotation_axis or dict()
        for i, (name, order) in enumerate(available_axises.items()):
            rot_axis_index = tp.Dcc.ROTATION_AXES.index(order.lower())
            self._set_rot_axis_common_btn_menu.addAction(
                '({})   {}'.format(order, name), partial(self._controller.change_rotation_order, rot_axis_index))

    def _on_rotation_axis_changed(self, index):
        self._set_rot_axis_box.setCurrentIndex(index)


class RotationAxistModel(QObject, object):

    rotationAxisChanged = Signal(int)
    affectChildrenChanged = Signal(bool)

    def __init__(self):
        super(RotationAxistModel, self).__init__()

        self._available_rotation_axis = OrderedDict({
            'Wrist': 'YXZ',
            'Finger': 'XYZ',
            'Spine': 'ZYX',
            'Hips': 'ZYX',
            'Root': 'ZYX',
            'Upper Leg': 'ZYX',
            'Knee': 'YXZ',
            'Ankle': 'XZY'
        })

        self._rotation_axis = 0
        self._affect_children = False

    @property
    def available_rotation_axis(self):
        return self._available_rotation_axis

    @property
    def rotation_axis(self):
        return self._rotation_axis

    @rotation_axis.setter
    def rotation_axis(self, value):
        self._rotation_axis = int(value)
        self.rotationAxisChanged.emit(value)

    @property
    def affect_children(self):
        return self._affect_children

    @affect_children.setter
    def affect_children(self, flag):
        self._affect_children = bool(flag)
        self.affectChildrenChanged.emit(self._affect_children)


class RotationAxisController(object):
    def __init__(self, client, model):
        super(RotationAxisController, self).__init__()

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

    def change_rotation_order(self, rotation_order_axis):
        self._model.rotation_axis = rotation_order_axis

    def change_affect_children(self, flag):
        self._model.affect_children = flag

    def set_rotation_axis(self):
        return self._client.set_rotation_axis(
            rotation_axis=self._model.rotation_axis, affect_children=self._model.affect_children)


def rotation_axis(client, parent=None):

    model = RotationAxistModel()
    controller = RotationAxisController(client=client, model=model)
    view = RotationAxisView(model=model, controller=controller, parent=parent)

    return view

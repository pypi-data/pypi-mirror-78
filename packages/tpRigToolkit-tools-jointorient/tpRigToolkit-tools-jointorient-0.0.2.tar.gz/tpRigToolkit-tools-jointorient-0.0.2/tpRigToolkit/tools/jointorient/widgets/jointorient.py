#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains joint orient widget implementation
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
from tpDcc.libs.qt.widgets import layouts, buttons, spinbox, dividers, group, checkbox

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-jointorient')


class JointOrientView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(JointOrientView, self).__init__(parent=parent)

        self.refresh()

    def ui(self):
        super(JointOrientView, self).ui()

        aim_axis_box = group.BaseGroup(layout_orientation=Qt.Horizontal, layout_spacing=8, parent=self)
        aim_axis_box.setTitle('Aim Axis')
        self._aim_x_radio = buttons.BaseRadioButton(' X ', parent=self)
        self._aim_y_radio = buttons.BaseRadioButton(' Y ', parent=self)
        self._aim_z_radio = buttons.BaseRadioButton(' Z ', parent=self)
        self._aim_rev_cbx = checkbox.BaseCheckBox('Reverse', parent=self)
        aim_axis_box.addWidget(self._aim_x_radio)
        aim_axis_box.addWidget(self._aim_y_radio)
        aim_axis_box.addWidget(self._aim_z_radio)
        aim_axis_box.addWidget(self._aim_rev_cbx)
        self._aim_axis_boxes = [self._aim_x_radio, self._aim_y_radio, self._aim_z_radio]

        up_axis_box = group.BaseGroup(layout_orientation=Qt.Horizontal, layout_spacing=8, parent=self)
        up_axis_box.setTitle('Up Axis')
        self._up_x_radio = buttons.BaseRadioButton(' X ', parent=self)
        self._up_y_radio = buttons.BaseRadioButton(' Y ', parent=self)
        self._up_z_radio = buttons.BaseRadioButton(' Z ', parent=self)
        self._up_rev_cbx = checkbox.BaseCheckBox('Reverse', parent=self)
        up_axis_box.addWidget(self._up_x_radio)
        up_axis_box.addWidget(self._up_y_radio)
        up_axis_box.addWidget(self._up_z_radio)
        up_axis_box.addWidget(self._up_rev_cbx)
        self._up_axis_boxes = [self._up_x_radio, self._up_y_radio, self._up_z_radio]

        up_world_axis_box = group.BaseGroup(layout_orientation=Qt.Horizontal, layout_spacing=2, parent=self)
        up_world_axis_box.setTitle('Up World Axis')
        self._up_world_x_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._up_world_y_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._up_world_z_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._up_world_x_spin.setDecimals(3)
        self._up_world_y_spin.setDecimals(3)
        self._up_world_z_spin.setDecimals(3)
        self._up_world_x_spin.setRange(-360, 360)
        self._up_world_y_spin.setRange(-360, 360)
        self._up_world_z_spin.setRange(-360, 360)
        self._up_world_x_btn = buttons.get_axis_button('X', parent=self, as_tool_button=False)
        self._up_world_y_btn = buttons.get_axis_button('Y', parent=self, as_tool_button=False)
        self._up_world_z_btn = buttons.get_axis_button('Z', parent=self, as_tool_button=False)
        up_world_axis_box.addWidget(self._up_world_x_spin)
        up_world_axis_box.addWidget(self._up_world_y_spin)
        up_world_axis_box.addWidget(self._up_world_z_spin)
        up_world_axis_box.addWidget(self._up_world_x_btn)
        up_world_axis_box.addWidget(self._up_world_y_btn)
        up_world_axis_box.addWidget(self._up_world_z_btn)

        joint_orient_btn_layout = layouts.HorizontalLayout()
        joint_orient_btn_layout.addStretch()
        self._joint_orient_btn = buttons.BaseButton('Apply', parent=self)
        self._reset_orient_to_world_btn = buttons.BaseButton('Reset to World', parent=self)
        self._hierarchy_cbx = checkbox.BaseCheckBox('Hierarchy', parent=self)
        self._joint_orient_btn.setMaximumWidth(80)
        joint_orient_btn_layout.addWidget(self._joint_orient_btn)
        joint_orient_btn_layout.addWidget(self._reset_orient_to_world_btn)
        joint_orient_btn_layout.addWidget(self._hierarchy_cbx)
        joint_orient_btn_layout.addStretch()

        self.main_layout.addWidget(aim_axis_box)
        self.main_layout.addWidget(up_axis_box)
        self.main_layout.addWidget(up_world_axis_box)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addLayout(joint_orient_btn_layout)

    def setup_signals(self):
        self._aim_x_radio.clicked.connect(partial(self._controller.change_aim_axis, 0))
        self._aim_y_radio.clicked.connect(partial(self._controller.change_aim_axis, 1))
        self._aim_z_radio.clicked.connect(partial(self._controller.change_aim_axis, 2))
        self._aim_rev_cbx.toggled.connect(self._controller.change_aim_axis_reverse)
        self._up_x_radio.clicked.connect(partial(self._controller.change_up_axis, 0))
        self._up_y_radio.clicked.connect(partial(self._controller.change_up_axis, 1))
        self._up_z_radio.clicked.connect(partial(self._controller.change_up_axis, 2))
        self._up_rev_cbx.toggled.connect(self._controller.change_up_axis_reverse)
        self._up_world_x_spin.valueChanged.connect(self._controller.change_up_world_axis_x)
        self._up_world_y_spin.valueChanged.connect(self._controller.change_up_world_axis_y)
        self._up_world_z_spin.valueChanged.connect(self._controller.change_up_world_axis_z)
        self._hierarchy_cbx.toggled.connect(self._controller.change_apply_hierarchy)

        self._up_world_x_btn.clicked.connect(self._controller.set_up_world_axis_to_x)
        self._up_world_y_btn.clicked.connect(self._controller.set_up_world_axis_to_y)
        self._up_world_z_btn.clicked.connect(self._controller.set_up_world_axis_to_z)
        self._joint_orient_btn.clicked.connect(self._controller.orient_joints)
        self._reset_orient_to_world_btn.clicked.connect(self._controller.reset_joints_orient_to_world)

        self._model.aimAxisChanged.connect(self._on_aim_axis_changed)
        self._model.aimAxisReverseChanged.connect(self._aim_rev_cbx.setChecked)
        self._model.upAxisChanged.connect(self._on_up_axis_changed)
        self._model.upAxisReverseChanged.connect(self._up_rev_cbx.setChecked)
        self._model.upWorldAxisXChanged.connect(self._up_world_x_spin.setValue)
        self._model.upWorldAxisYChanged.connect(self._up_world_y_spin.setValue)
        self._model.upWorldAxisZChanged.connect(self._up_world_z_spin.setValue)
        self._model.applyToHierarchyChanged.connect(self._hierarchy_cbx.setChecked)

    def refresh(self):
        self._aim_axis_boxes[self._model.aim_axis].setChecked(True)
        self._aim_rev_cbx.setChecked(self._model.aim_axis_reverse)
        self._up_axis_boxes[self._model.up_axis].setChecked(True)
        self._up_rev_cbx.setChecked(self._model.up_axis_reverse)
        self._up_world_x_spin.setValue(self._model.up_world_axis_x)
        self._up_world_y_spin.setValue(self._model.up_world_axis_y)
        self._up_world_z_spin.setValue(self._model.up_world_axis_z)
        self._hierarchy_cbx.setChecked(self._model.apply_to_hierarchy)

    def _on_aim_axis_changed(self, value):
        self._aim_axis_boxes[value].setChecked(True)

    def _on_up_axis_changed(self, value):
        self._up_axis_boxes[value].setChecked(True)


class JointOrientModel(QObject, object):

    aimAxisChanged = Signal(int)
    aimAxisReverseChanged = Signal(bool)
    upAxisChanged = Signal(int)
    upAxisReverseChanged = Signal(bool)
    upWorldAxisXChanged = Signal(float)
    upWorldAxisYChanged = Signal(float)
    upWorldAxisZChanged = Signal(float)
    applyToHierarchyChanged = Signal(bool)

    def __init__(self):
        super(JointOrientModel, self).__init__()

        self._aim_axis = 0
        self._aim_axis_reverse = False
        self._up_axis = 1
        self._up_axis_reverse = False
        self._up_world_axis_x = 1.0
        self._up_world_axis_y = 0.0
        self._up_world_axis_z = 0.0
        self._apply_to_hierarchy = True

    @property
    def aim_axis(self):
        return self._aim_axis

    @aim_axis.setter
    def aim_axis(self, value):
        self._aim_axis = int(value)
        self.aimAxisChanged.emit(self._aim_axis)

    @property
    def aim_axis_reverse(self):
        return self._aim_axis_reverse

    @aim_axis_reverse.setter
    def aim_axis_reverse(self, flag):
        self._aim_axis_reverse = bool(flag)
        self.aimAxisReverseChanged.emit(self._aim_axis_reverse)

    @property
    def up_axis(self):
        return self._up_axis

    @up_axis.setter
    def up_axis(self, value):
        self._up_axis = int(value)
        self.upAxisChanged.emit(self._up_axis)

    @property
    def up_axis_reverse(self):
        return self._up_axis_reverse

    @up_axis_reverse.setter
    def up_axis_reverse(self, flag):
        self._up_axis_reverse = bool(flag)
        self.upAxisReverseChanged.emit(self._up_axis_reverse)

    @property
    def up_world_axis_x(self):
        return self._up_world_axis_x

    @up_world_axis_x.setter
    def up_world_axis_x(self, value):
        self._up_world_axis_x = float(value)
        self.upWorldAxisXChanged.emit(self._up_world_axis_x)

    @property
    def up_world_axis_y(self):
        return self._up_world_axis_y

    @up_world_axis_y.setter
    def up_world_axis_y(self, value):
        self._up_world_axis_y = float(value)
        self.upWorldAxisYChanged.emit(self._up_world_axis_y)

    @property
    def up_world_axis_z(self):
        return self._up_world_axis_z

    @up_world_axis_z.setter
    def up_world_axis_z(self, value):
        self._up_world_axis_z = float(value)
        self.upWorldAxisZChanged.emit(self._up_world_axis_z)

    @property
    def apply_to_hierarchy(self):
        return self._apply_to_hierarchy

    @apply_to_hierarchy.setter
    def apply_to_hierarchy(self, flag):
        self._apply_to_hierarchy = bool(flag)
        self.applyToHierarchyChanged.emit(self._apply_to_hierarchy)


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

    def change_aim_axis(self, value):
        self._model.aim_axis = value

    def change_aim_axis_reverse(self, flag):
        self._model.aim_axis_reverse = flag

    def change_up_axis(self, value):
        self._model.up_axis = value

    def change_up_axis_reverse(self, flag):
        self._model.up_axis_reverse = flag

    def change_up_world_axis_x(self, value):
        self._model.up_world_axis_x = value

    def change_up_world_axis_y(self, value):
        self._model.up_world_axis_y = value

    def change_up_world_axis_z(self, value):
        self._model.up_world_axis_z = value

    def change_apply_hierarchy(self, flag):
        self._model.apply_to_hierarchy = flag

    def set_up_world_axis_to_x(self):
        self._model.up_world_axis_x = 1.0
        self._model.up_world_axis_y = 0.0
        self._model.up_world_axis_z = 0.0

    def set_up_world_axis_to_y(self):
        self._model.up_world_axis_x = 0.0
        self._model.up_world_axis_y = 1.0
        self._model.up_world_axis_z = 0.0

    def set_up_world_axis_to_z(self):
        self._model.up_world_axis_x = 0.0
        self._model.up_world_axis_y = 0.0
        self._model.up_world_axis_z = 1.0

    def orient_joints(self):
        return self._client.orient_joints(
            aim_axis_index=self._model.axim_axis, aim_axis_reverse=self._model.aim_axis_reverse,
            up_axis_index=self._model.up_axis, up_axis_reverse=self._model.up_axis_reverse,
            up_world_axis_x=self._model.up_world_axis_x, up_world_axis_y=self._model.up_world_axis_y,
            up_world_axis_z=self._model.up_world_axis_z, apply_to_hierarchy=self._model.apply_to_hierarchy)

    def reset_joints_orient_to_world(self):
        return self._client.reset_joints_orient_to_world(apply_to_hierarchy=self._model.apply_to_hierarchy)


def joint_orient(client, parent=None):
    model = JointOrientModel()
    controller = JointOrientController(client=client, model=model)
    view = JointOrientView(model=model, controller=controller, parent=parent)

    return view

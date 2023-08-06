#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains manual joint orient widget implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, label, spinbox, buttons, group, dividers, checkbox


class ManualJointOrientView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(ManualJointOrientView, self).__init__(parent=parent)

        self.refresh()

    def ui(self):
        super(ManualJointOrientView, self).ui()

        manual_joint_ori_layout = layouts.HorizontalLayout()
        manual_joint_ori_lbl = label.BaseLabel('  X  Y  Z  ', parent=self)
        self._manual_joint_ori_x_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._manual_joint_ori_y_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._manual_joint_ori_z_spin = spinbox.BaseDoubleSpinBox(parent=self)
        self._manual_joint_ori_x_spin.setDecimals(3)
        self._manual_joint_ori_y_spin.setDecimals(3)
        self._manual_joint_ori_z_spin.setDecimals(3)
        self._manual_joint_ori_x_spin.setRange(-360, 360)
        self._manual_joint_ori_y_spin.setRange(-360, 360)
        self._manual_joint_ori_z_spin.setRange(-360, 360)
        self._manual_joint_ori_x_spin.setLocale(QLocale.English)
        self._manual_joint_ori_y_spin.setLocale(QLocale.English)
        self._manual_joint_ori_z_spin.setLocale(QLocale.English)
        self._manual_joint_ori_reset_btn = buttons.BaseButton('Reset', parent=self)
        manual_joint_ori_layout.addWidget(manual_joint_ori_lbl)
        manual_joint_ori_layout.addWidget(self._manual_joint_ori_x_spin)
        manual_joint_ori_layout.addWidget(self._manual_joint_ori_y_spin)
        manual_joint_ori_layout.addWidget(self._manual_joint_ori_z_spin)
        manual_joint_ori_layout.addWidget(self._manual_joint_ori_reset_btn)

        manual_joint_splitter_layout = layouts.VerticalLayout()
        degree_box = group.BaseGroup(parent=self, layout_orientation=Qt.Horizontal)
        degree_box.setStyleSheet("border:0px;")
        manual_joint_splitter_layout.addWidget(degree_box)
        self._degrees_checks = list()
        for degree in self._model.available_degrees:
            degree_radio = buttons.BaseRadioButton(str(degree), parent=self)
            degree_box.addWidget(degree_radio)
            self._degrees_checks.append(degree_radio)

        manual_joint_ori_buttons_layout = layouts.HorizontalLayout(spacing=5, margins=(2, 2, 2, 2))
        self._manual_joint_ori_add_btn = buttons.BaseButton('Add', parent=self)
        self._manual_joint_ori_subtract_btn = buttons.BaseButton('Subract', parent=self)
        self._manual_joint_ori_set_btn = buttons.BaseButton('Set', parent=self)
        self._manual_joint_ori_set_cbx = checkbox.BaseCheckBox('Affect children', parent=self)
        manual_joint_ori_buttons_layout.addWidget(self._manual_joint_ori_add_btn)
        manual_joint_ori_buttons_layout.addWidget(self._manual_joint_ori_subtract_btn)
        manual_joint_ori_buttons_layout.addWidget(self._manual_joint_ori_set_btn)
        manual_joint_ori_buttons_layout.addWidget(self._manual_joint_ori_set_cbx)

        set_rot_axis_widget = QWidget()
        set_rot_axis_widget.setLayout(layouts.VerticalLayout())
        set_rot_axis_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        set_rot_axis_widget.layout().setContentsMargins(5, 5, 5, 5)
        set_rot_axis_widget.layout().setSpacing(10)

        self.main_layout.addLayout(manual_joint_ori_layout)
        self.main_layout.addLayout(manual_joint_splitter_layout)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addLayout(manual_joint_ori_buttons_layout)
        self.main_layout.addWidget(set_rot_axis_widget)

    def setup_signals(self):
        self._manual_joint_ori_x_spin.valueChanged.connect(self._on_change_x_axis)
        self._manual_joint_ori_y_spin.valueChanged.connect(self._on_change_y_axis)
        self._manual_joint_ori_z_spin.valueChanged.connect(self._on_change_z_axis)
        for i, cbx in enumerate(self._degrees_checks):
            cbx.clicked.connect(partial(self._controller.change_degree, i))
        self._manual_joint_ori_set_cbx.toggled.connect(self._controller.change_affect_children)

        self._manual_joint_ori_reset_btn.clicked.connect(self._controller.reset_axis_values)
        self._manual_joint_ori_add_btn.clicked.connect(partial(self._controller.manual_orient_joints, 'add'))
        self._manual_joint_ori_subtract_btn.clicked.connect(partial(self._controller.manual_orient_joints, 'subtract'))
        self._manual_joint_ori_set_btn.clicked.connect(self._controller.set_manual_orient_joints)

        self._model.xAxisChanged.connect(self._manual_joint_ori_x_spin.setValue)
        self._model.yAxisChanged.connect(self._manual_joint_ori_y_spin.setValue)
        self._model.zAxisChanged.connect(self._manual_joint_ori_z_spin.setValue)
        self._model.degreesChanged.connect(self._on_degrees_changed)
        self._model.affectChildrenChanged.connect(self._manual_joint_ori_set_cbx.setChecked)

    def refresh(self):
        self._manual_joint_ori_x_spin.setValue(self._model.x_axis)
        self._manual_joint_ori_y_spin.setValue(self._model.y_axis)
        self._manual_joint_ori_z_spin.setValue(self._model.z_axis)
        self._degrees_checks[self._model.degrees].setChecked(True)
        self._manual_joint_ori_set_cbx.setChecked(self._model.affect_children)

    def _on_change_x_axis(self, value):
        self._manual_joint_ori_x_spin.blockSignals(True)
        try:
            self._controller.change_x_axis_value(value)
        finally:
            self._manual_joint_ori_x_spin.blockSignals(False)

    def _on_change_y_axis(self, value):
        self._manual_joint_ori_y_spin.blockSignals(True)
        try:
            self._controller.change_y_axis_value(value)
        finally:
            self._manual_joint_ori_y_spin.blockSignals(False)

    def _on_change_z_axis(self, value):
        self._manual_joint_ori_z_spin.blockSignals(True)
        try:
            self._controller.change_z_axis_value(value)
        finally:
            self._manual_joint_ori_z_spin.blockSignals(False)

    def _on_degrees_changed(self, index):
        self._degrees_checks[index].setChecked(True)


class ManualOrientJointModel(QObject, object):

    xAxisChanged = Signal(float)
    yAxisChanged = Signal(float)
    zAxisChanged = Signal(float)
    degreesChanged = Signal(int)
    affectChildrenChanged = Signal(bool)

    def __init__(self):
        super(ManualOrientJointModel, self).__init__()

        self._available_degrees = [1, 5, 10, 20, 45, 90, 180]
        self._x_axis = 0.0
        self._y_axis = 0.0
        self._z_axis = 0.0
        self._degrees = 5
        self._affect_children = False

    @property
    def available_degrees(self):
        return self._available_degrees

    @property
    def x_axis(self):
        return self._x_axis

    @x_axis.setter
    def x_axis(self, value):
        self._x_axis = float(value)
        self.xAxisChanged.emit(self._x_axis)

    @property
    def y_axis(self):
        return self._y_axis

    @y_axis.setter
    def y_axis(self, value):
        self._y_axis = float(value)
        self.yAxisChanged.emit(self._y_axis)

    @property
    def z_axis(self):
        return self._z_axis

    @z_axis.setter
    def z_axis(self, value):
        self._z_axis = float(value)
        self.zAxisChanged.emit(self._z_axis)

    @property
    def degrees(self):
        return self._degrees

    @degrees.setter
    def degrees(self, value):
        self._degrees = int(value)
        self.degreesChanged.emit(self._degrees)

    @property
    def affect_children(self):
        return self._affect_children

    @affect_children.setter
    def affect_children(self, flag):
        self._affect_children = bool(flag)
        self.affectChildrenChanged.emit(self._affect_children)


class ManualOrientJointController(object):
    def __init__(self, client, model):
        super(ManualOrientJointController, self).__init__()

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

    def change_x_axis_value(self, value):

        if value == 0:
            new_value = 0.0
        else:
            degrees = self._model.available_degrees[self._model.degrees]
            new_value = self._model.x_axis + degrees if value > self._model.x_axis else self._model.x_axis - degrees

        self._model.x_axis = new_value

    def change_y_axis_value(self, value):
        if value == 0:
            new_value = 0.0
        else:
            degrees = self._model.available_degrees[self._model.degrees]
            new_value = self._model.y_axis + degrees if value > self._model.y_axis else self._model.y_axis - degrees

        self._model.y_axis = new_value

    def change_z_axis_value(self, value):
        if value == 0:
            new_value = 0.0
        else:
            degrees = self._model.available_degrees[self._model.degrees]
            new_value = self._model.z_axis + degrees if value > self._model.z_axis else self._model.z_axis - degrees

        self._model.z_axis = new_value

    def change_degree(self, value):
        self._model.degrees = value

    def change_affect_children(self, flag):
        self._model.affect_children = flag

    def reset_axis_values(self):
        self._model.x_axis = 0.0
        self._model.y_axis = 0.0
        self._model.z_axis = 0.0

    def manual_orient_joints(self, orient_type):
        return self._client.manual_orient_joints(
            orient_type=orient_type, x_axis=self._model.x_axis, y_axis=self._model.y_axis, z_axis=self._model.z_axis,
            affect_children=self._model.affect_children
        )

    def set_manual_orient_joints(self):
        return self._client.set_manual_joints(
            x_axis=self._model.x_axis, y_axis=self._model.y_axis, z_axis=self._model.z_axis,
            affect_children=self._model.affect_children
        )


def manual_joint_orient(client, parent=None):

    model = ManualOrientJointModel()
    controller = ManualOrientJointController(client=client, model=model)
    view = ManualJointOrientView(model=model, controller=controller, parent=parent)

    return view

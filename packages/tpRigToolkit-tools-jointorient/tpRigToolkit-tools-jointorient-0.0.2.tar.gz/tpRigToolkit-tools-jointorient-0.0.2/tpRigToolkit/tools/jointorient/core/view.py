#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Joint Orient widget view class implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"


from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import expandables

from tpRigToolkit.tools.jointorient.widgets import jointorient, manualjointorient, rotationaxis, jointutils


class JointOrientView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(JointOrientView, self).__init__(parent=parent)

        self.refresh()

    def ui(self):
        super(JointOrientView, self).ui()

        self._expander = expandables.ExpanderWidget()
        self.main_layout.addWidget(self._expander)

        self._orient_joint = jointorient.joint_orient(client=self._controller.client, parent=self)
        self._manual_orient_joint = manualjointorient.manual_joint_orient(client=self._controller.client, parent=self)
        self._rotation_axis = rotationaxis.rotation_axis(client=self._controller.client, parent=self)
        self._joint_utils = jointutils.joint_utils(client=self._controller.client, parent=self)

        self._expander.addItem('Joint Utilities', self._joint_utils)
        self._expander.addItem('Joint Orient', self._orient_joint)
        self._expander.addItem('Manual Orient', self._manual_orient_joint, collapsed=False)
        self._expander.addItem('Set Rotation Axis', self._rotation_axis, collapsed=False)

    def refresh(self):
        for widget in [self._orient_joint, self._manual_orient_joint, self._rotation_axis]:
            widget.refresh()

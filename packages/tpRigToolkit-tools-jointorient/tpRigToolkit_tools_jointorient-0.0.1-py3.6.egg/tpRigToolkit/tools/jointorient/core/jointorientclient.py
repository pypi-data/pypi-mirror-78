#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpRigToolkit-tools-jointorient client implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from tpDcc.core import client


class JointOrientClient(client.DccClient, object):

    PORT = 17231

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def orient_joints(
            self, aim_axis_index, aim_axis_reverse, up_axis_index, up_axis_reverse,
            up_world_axis_x, up_world_axis_y, up_world_axis_z, apply_to_hierarchy):
        cmd = {
            'cmd': 'orient_joints',
            'aim_axis_index': aim_axis_index,
            'aim_axis_reverse': aim_axis_reverse,
            'up_axis_index': up_axis_index,
            'up_axis_reverse': up_axis_reverse,
            'up_world_axis_x': up_world_axis_x,
            'up_world_axis_y': up_world_axis_y,
            'up_world_axis_z': up_world_axis_z,
            'apply_to_hierarchy': apply_to_hierarchy
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def reset_joints_orient_to_world(self, apply_to_hierarchy):
        cmd = {
            'cmd': 'reset_joints_orient_to_world',
            'apply_to_hierarchy': apply_to_hierarchy
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def manual_orient_joints(self, orient_type, x_axis, y_axis, z_axis, affect_children):
        cmd = {
            'cmd': 'manual_orient_joints',
            'orient_type': orient_type,
            'x_axis': x_axis,
            'y_axis': y_axis,
            'z_axis': z_axis,
            'affect_children': affect_children,
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def set_manual_joints(self, x_axis, y_axis, z_axis, affect_children):
        cmd = {
            'cmd': 'set_manual_joints',
            'x_axis': x_axis,
            'y_axis': y_axis,
            'z_axis': z_axis,
            'affect_children': affect_children,
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def set_rotation_axis(self, rotation_axis, affect_children):
        cmd = {
            'cmd': 'set_rotation_axis',
            'rotation_axis': rotation_axis,
            'affect_children': affect_children
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def set_local_rotation_axis(self, state):
        cmd = {
            'cmd': 'set_local_rotation_axis',
            'state': state
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def select_hierarchy(self):
        cmd = {
            'cmd': 'select_hierarchy'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

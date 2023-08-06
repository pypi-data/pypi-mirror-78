#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpRigToolkit-tools-jointorient server implementation
"""

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import tpDcc as tp
from tpDcc.core import server

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-jointorient')


class JointOrientServer(server.DccServer, object):

    PORT = 17231

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'orient_joints':
            self.orient_joints(data_dict, reply_dict)
        elif command_name == 'reset_joints_orient_to_world':
            self.reset_joints_orient_to_world(data_dict, reply_dict)
        elif command_name == 'manual_orient_joints':
            self.manual_orient_joints(data_dict, reply_dict)
        elif command_name == 'set_manual_orient_joints':
            self.set_manual_orient_joints(data_dict, reply_dict)
        elif command_name == 'set_rotation_axis':
            self.set_rotation_axis(data_dict, reply_dict)
        elif command_name == 'set_local_rotation_axis':
            self.set_local_rotation_axis(data_dict, reply_dict)
        elif command_name == 'select_hierarchy':
            self.select_hierarchy(data_dict, reply_dict)
        else:
            super(JointOrientServer, self)._process_command(command_name, data_dict, reply_dict)

    @tp.Dcc.get_undo_decorator()
    def orient_joints(self, data, reply):
        aim_axis_index = data.get('aim_axis_index', 0.0)
        aim_axis_reverse = data.get('aim_axis_reverse', False)
        up_axis_index = data.get('up_axis_index', 0.0)
        up_axis_reverse = data.get('up_axis_reverse', False)
        up_world_axis_x = data.get('up_world_axis_x', 0.0)
        up_world_axis_y = data.get('up_world_axis_y', 0.0)
        up_world_axis_z = data.get('up_world_axis_z', 0.0)
        apply_to_hierarchy = data.get('apply_to_hierarchy', False)

        reset_joints = list()

        # Get up and aim axis
        aim_axis = [0, 0, 0]
        up_axis = [0, 0, 0]
        world_up_axis = [up_world_axis_x, up_world_axis_y, up_world_axis_z]

        if aim_axis_index == up_axis_index:
            LOGGER.warning('aim and up axis are the same, maybe orientation wont work correctly!')

        aim_axis_reverse_value = 1.0 if not aim_axis_reverse else -1.0
        up_axis_reverse_value = 1.0 if not up_axis_reverse else -1.0

        aim_axis[aim_axis_index] = aim_axis_reverse_value
        up_axis[up_axis_index] = up_axis_reverse_value

        # Get selected joints
        if apply_to_hierarchy:
            tp.Dcc.select_hierarchy()

        joints = tp.Dcc.selected_nodes_of_type(node_type='joint', full_path=False)
        if not joints:
            reply['msg'] = 'No joints selected'
            reply['success'] = False
            return

        for jnt in reversed(joints):
            childs = tp.Dcc.list_children(jnt, all_hierarchy=False, children_type=['transform', 'joint'])

            # If the joints has direct childs, unparent that childs and store names
            if childs:
                if len(childs) > 0:
                    childs = tp.Dcc.set_parent_to_world(childs)

            # Get parent of this joints for later use
            parent = ''
            parents = tp.Dcc.node_parent(jnt)
            if parents:
                parent = parents[0]

            # Aim to the child
            aim_target = ''
            if childs:
                for child in childs:
                    if tp.Dcc.node_type(child) == 'joint':
                        aim_target = child
                        break

            if aim_target != '':

                # Apply an aim constraint from the joint to its child (target)
                tp.Dcc.delete_object(tp.Dcc.create_aim_constraint(
                    jnt, aim_target, aim_axis=aim_axis, up_axis=up_axis, world_up_axis=world_up_axis,
                    world_up_type='vector', weight=1.0))

                # Clear joint axis
                tp.Dcc.zero_scale_joint(jnt)
                tp.Dcc.freeze_transforms(jnt, preserve_pivot_transforms=True)

            elif parent != '':
                reset_joints.append(jnt)

            # Reparent child
            if childs:
                if len(childs) > 0:
                    tp.Dcc.set_parent(childs, jnt)

        for jnt in reset_joints:
            # If there is no target, the joint will take its parent orientation
            for axis in ['x', 'y', 'z']:
                tp.Dcc.set_attribute_value(
                    jnt, 'jointOrient{}'.format(axis.upper()), tp.Dcc.get_attribute_value(jnt, 'r{}'.format(axis)))
                tp.Dcc.set_attribute_value(jnt, 'r{}'.format(axis), 0)

        tp.Dcc.select_object(joints, replace_selection=True)

        reply['success'] = True

    @tp.Dcc.get_undo_decorator()
    def reset_joints_orient_to_world(self, data, reply):
        apply_to_hierarchy = data.get('apply_to_hierarchy', False)

        if apply_to_hierarchy:
            tp.Dcc.select_hierarchy()

        joints = tp.Dcc.selected_nodes_of_type(node_type='joint', full_path=False)
        if not joints:
            reply['msg'] = 'No joints selected'
            reply['success'] = False
            return

        for jnt in reversed(joints):
            childs = tp.Dcc.list_children(jnt, all_hierarchy=False, children_type=['transform', 'joint'])

            # If the joints has direct childs, unparent that childs and store names
            if childs:
                if len(childs) > 0:
                    childs = tp.Dcc.set_parent_to_world(childs)

            # Get parent of this joints for later use
            parent = tp.Dcc.node_parent(jnt, full_path=False) or ''

            if parent:
                tp.Dcc.set_parent_to_world(jnt)

            # Clear joint axis
            tp.Dcc.zero_scale_joint(jnt)
            tp.Dcc.freeze_transforms(jnt, preserve_pivot_transforms=True)
            tp.Dcc.zero_orient_joint(jnt)

            # Reparent
            if parent:
                tp.Dcc.set_parent(jnt, parent)

            # Reparent child
            if childs:
                if len(childs) > 0:
                    tp.Dcc.set_parent(childs, jnt)

        tp.Dcc.select_object(joints, replace_selection=True)

        reply['success'] = True

    @tp.Dcc.get_undo_decorator()
    def manual_orient_joints(self, data, reply):

        orient_type = data.get('orient_type', 'add')
        x_axis = data.get('x_axis', 0.0)
        y_axis = data.get('y_axis', 0.0)
        z_axis = data.get('z_axis', 0.0)
        affect_children = data.get('affect_children', False)

        if orient_type == 'add':
            tweak = 1.0
        else:
            tweak = -1.0

        tweak_rot = [x_axis * tweak, y_axis * tweak, z_axis * tweak]

        joints = tp.Dcc.selected_nodes_of_type(node_type='joint')
        if not joints:
            return

        for jnt in joints:
            tp.Dcc.set_node_rotation_axis_in_object_space(jnt, tweak_rot[0], tweak_rot[1], tweak_rot[2])
            tp.Dcc.zero_scale_joint(jnt)
            tp.Dcc.freeze_transforms(jnt, preserve_pivot_transforms=True)

            if affect_children:
                childs = tp.Dcc.list_children(
                    jnt, children_type=['transform', 'joint'], full_path=False, all_hierarchy=True) or list()
                for child in childs:
                    parent = tp.Dcc.node_parent(child)
                    tp.Dcc.set_parent_to_world(child)
                    tp.Dcc.set_node_rotation_axis_in_object_space(child, tweak_rot[0], tweak_rot[1], tweak_rot[2])
                    tp.Dcc.zero_scale_joint(child)
                    tp.Dcc.freeze_transforms(child, preserve_pivot_transforms=True)
                    tp.Dcc.set_parent(child, parent)

        tp.Dcc.select_object(joints, replace_selection=True)

        reply['success'] = True

    @tp.Dcc.get_undo_decorator()
    def set_manual_orient_joints(self, data, reply):
        x_axis = data.get('x_axis', 0.0)
        y_axis = data.get('y_axis', 0.0)
        z_axis = data.get('z_axis', 0.0)
        affect_children = data.get('affect_children', False)

        childs = list()

        tweak_rot = [x_axis, y_axis, z_axis]

        joints = tp.Dcc.selected_nodes_of_type(node_type='joint', full_path=False)
        if not joints:
            return

        for jnt in joints:
            if not affect_children:
                childs = tp.Dcc.list_children(
                    jnt, children_type=['transform', 'joint'], full_path=False, all_hierarchy=False) or list()
                for child in childs:
                    tp.Dcc.set_parent_to_world(child)

            # Set the rotation axis
            for i, axis in enumerate(['x', 'y', 'z']):
                tp.Dcc.set_attribute_value(jnt, 'jointOrient{}'.format(axis.upper()), tweak_rot[i])

            # Clear joint axis
            tp.Dcc.zero_scale_joint(jnt)
            tp.Dcc.freeze_transforms(jnt, preserve_pivot_transforms=True)

            if childs:
                for child in childs:
                    tp.Dcc.set_parent(child, jnt)

        tp.Dcc.select_object(joints, replace_selection=True)

        reply['success'] = True

    @tp.Dcc.get_undo_decorator()
    def set_rotation_axis(self, data, reply):
        rotation_axis = data.get('rotation_axis', '')
        affect_children = data.get('affect_children', False)

        sel = tp.Dcc.selected_nodes_of_type(node_type=['joint', 'transform']) or list()
        for obj in sel:
            tp.Dcc.set_rotation_axis(obj, rotation_axis)
            if affect_children:
                childs = tp.Dcc.list_children(
                    obj, children_type=['transform', 'joint'], full_path=True, all_hierarchy=True) or list()
                for child in childs:
                    tp.Dcc.set_rotation_axis(child, rotation_axis)

        reply['success'] = True

    @staticmethod
    @tp.Dcc.get_undo_decorator()
    @tp.Dcc.get_repeat_last_decorator(__name__ + '.JointOrientServer')
    def set_local_rotation_axis(data, reply):
        state = data.get('state', False)

        sel = tp.Dcc.selected_nodes()
        for obj in sel:
            if tp.Dcc.attribute_exists(obj, 'displayLocalAxis'):
                tp.Dcc.set_attribute_value(obj, 'displayLocalAxis', state)

        reply['success'] = True

    @staticmethod
    @tp.Dcc.get_undo_decorator()
    @tp.Dcc.get_repeat_last_decorator(__name__ + '.JointOrientServer')
    def select_hierarchy(data, reply):

        sel = tp.Dcc.selected_nodes()

        for obj in sel:
            tp.Dcc.select_hierarchy(obj, add=True)

        reply['success'] = True

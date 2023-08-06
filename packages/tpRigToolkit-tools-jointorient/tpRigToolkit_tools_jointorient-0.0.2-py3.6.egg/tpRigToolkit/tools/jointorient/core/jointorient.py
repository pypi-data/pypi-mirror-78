#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool to orient joints quickly
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import importlib

import tpDcc as tp
from tpDcc.core import tool
from tpDcc.libs.qt.widgets import toolset

from tpRigToolkit.tools.jointorient.core import jointorientclient

# Defines ID of the tool
TOOL_ID = 'tpRigToolkit-tools-jointorient'


class JointOrientTool(tool.DccTool, object):
    def __init__(self, *args, **kwargs):
        super(JointOrientTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Joint Orient',
            'id': 'tpRigToolkit-tools-jointorient',
            'supported_dccs': {'maya': ['2017', '2018', '2019', '2020']},
            'logo': 'jointorient',
            'icon': 'jointorient',
            'tooltip': ' Tool to orient joints quickly',
            'tags': ['tpRigToolkit', 'joint', 'orient'],
            'logger_dir': os.path.join(os.path.expanduser('~'), 'tpRigToolkit', 'logs', 'tools'),
            'logger_level': 'INFO',
            'size': [425, 600]
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


class JointOrientToolset(toolset.ToolsetWidget, object):
    ID = TOOL_ID

    def __init__(self, *args, **kwargs):
        super(JointOrientToolset, self).__init__(*args, **kwargs)

    def setup_client(self):

        self._client = jointorientclient.JointOrientClient()
        self._client.signals.dccDisconnected.connect(self._on_dcc_disconnected)

        if not tp.is_standalone():
            dcc_mod_name = '{}.dccs.{}.jointorientserver'.format(TOOL_ID.replace('-', '.'), tp.Dcc.get_name())
            try:
                mod = importlib.import_module(dcc_mod_name)
                if hasattr(mod, 'JointOrientServer'):
                    server = mod.JointOrientServer(self, client=self._client, update_paths=False)
                    self._client.set_server(server)
                    self._update_client()
            except Exception as exc:
                tp.logger.warning(
                    'Impossible to launch ControlRig server! Error while importing: {} >> {}'.format(dcc_mod_name, exc))
                return
        else:
            self._update_client()

    def contents(self):

        from tpRigToolkit.tools.jointorient.core import model, view, controller

        joint_orient_model = model.JointOrientModel()
        joint_orient_controller = controller.JointOrientController(client=self._client, model=joint_orient_model)
        joint_orient_view = view.JointOrientView(
            model=joint_orient_model, controller=joint_orient_controller, parent=self)

        return [joint_orient_view]


if __name__ == '__main__':
    import tpDcc
    import tpDcc.loader

    tpDcc.loader.init(dev=False)

    tpDcc.ToolsMgr().launch_tool_by_id('tpRigToolkit-tools-jointorient')

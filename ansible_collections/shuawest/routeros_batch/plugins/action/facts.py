#!/usr/bin/python

from ansible.utils.display import Display
from typing import Dict
# from enum import Enum

from ansible.errors import AnsibleError, AnsibleAction, _AnsibleActionDone, AnsibleActionFail, AnsibleActionSkip
from ansible.plugins.action import ActionBase
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import cmd_spec
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import ros_paths

display = Display()


ROS_API_INFO = "community.routeros.api_info"

SCRIPT_PATH = "/system script"
REMOVE_FAILED_MSG = "no such item"

KEY_CHANGED = "changed"
KEY_FAILED = "failed"
KEY_MSG = "msg"

KEY_ROUTEROS = "routeros"
KEY_PATHS = "paths"
KEY_NAME = "name"
KEY_PATH = "path"
KEY_RESULT = "result"


def get_argument_spec():
    # routeros vars from https://docs.ansible.com/ansible/latest/collections/community/routeros/api_module.html
    argument_spec = dict(
        paths=dict(type='list', elements='dict', required=True, options={
            KEY_NAME: dict(type='str', required=True),
            KEY_PATH: dict(type='str', required=True),
        }),
        routeros=cmd_spec.get_routeros_spec(),
    )
    return argument_spec


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec=get_argument_spec(),
        )

        module = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try: 
            output = self.process(new_module_args, task_vars)
            return output
        except Exception as e:
            output = dict(failed=True, changed=False, msg=str(e), execption=e)
            return output


    def process(self, module_args, task_vars):
        routeros_vars = module_args[KEY_ROUTEROS]

        paths = module_args[KEY_PATHS]

        output = dict()
  
        # iterate through each path to call API and gather facts
        for pathkv in paths:
            name = pathkv[KEY_NAME]
            path = pathkv[KEY_PATH]

            # is_item_path = path in ros_paths.ROUTEROS_ITEM_PATHS or "/"+path in ros_paths.ROUTEROS_ITEM_PATHS:
       
            # fetch facts using api_info module for the path 
            path_facts = self.routeros_api_info(task_vars, routeros_vars, path)
            
            # add result to the output dictionary
            if KEY_RESULT in path_facts:
                output[name] = path_facts[KEY_RESULT]
            else:
                output[name] = dict()
            

        return output


    def routeros_api_info(self, sys_vars, routeros_vars, path):
        api_args = dict(**routeros_vars)
        api_args[KEY_PATH] = path

        api_result = self._execute_module(
            module_name=ROS_API_INFO, 
            module_args=api_args, 
            task_vars=sys_vars)

        return api_result


#!/usr/bin/python

from ansible.utils.display import Display
from typing import Dict
from enum import Enum

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
KEY_AS_KVPAIR = "as_keyvalue"
KEY_INCLUDE_NULL = "include_null"
KEY_NAME = "name"
KEY_VALUE = "value"
KEY_PATH = "path"
KEY_RESULT = "result"
KEY_ISNULL = "is_null"


def get_argument_spec():
    # routeros vars from https://docs.ansible.com/ansible/latest/collections/community/routeros/api_module.html
    argument_spec = dict(
        paths=dict(type='list', elements='dict', required=True, options={
            KEY_NAME: dict(type='str', required=True),
            KEY_PATH: dict(type='str', required=True),
        }),
        as_keyvalue=dict(type='bool', default=False),
        include_null=dict(type='bool', default=True),
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
            output = dict(failed=True, changed=False, msg=str(e), exception=e)
            return output


    def process(self, module_args, task_vars):
        routeros_vars = module_args[KEY_ROUTEROS]

        paths = module_args[KEY_PATHS]
        as_keyvalue = module_args[KEY_AS_KVPAIR]
        include_null = module_args[KEY_INCLUDE_NULL]

        output = dict()
  
        # iterate through each path to call API and gather facts
        for pathkv in paths:
            name = pathkv[KEY_NAME]
            path = pathkv[KEY_PATH]

            # determine if the path is recognized as a list or item
            known_path_type = cmd_spec.lookup_path_type(path)

            # fetch facts using api_info module for the path 
            path_output = self.routeros_api_info(task_vars, routeros_vars, path)
            
            raw_path_result = path_output[KEY_RESULT]
            path_result = process_result_item(raw_path_result, as_keyvalue, include_null)

            # determine the path type from the result - list (array) or item (dict)
            result_path_type = cmd_spec.PathType.UNRECOGNIZED.value
            if isinstance(path_result, list):
                result_path_type = cmd_spec.PathType.LIST.value
            elif isinstance(path_result, dict):
                result_path_type = cmd_spec.PathType.ITEM.value

            # check known path result type against actual result length
            if known_path_type == cmd_spec.PathType.ITEM.value and len(path_result) > 1:
                display.warning("Expected path '%s' to return a single item, but multiple were returned. Only including the first item in the output from: %s" % (path, known_path_type, path_result), True)

            # construct the itemized output for the name 
            output[name] = {
                'path': path,
                'path_type': known_path_type,
                'values': path_result,
            }               

        return output

    def routeros_api_info(self, sys_vars, routeros_vars, path):
        api_args = dict(**routeros_vars)
        api_args[KEY_PATH] = path

        api_result = self._execute_module(
            module_name=ROS_API_INFO, 
            module_args=api_args, 
            task_vars=sys_vars)

        return api_result


def process_result_item(raw_result, as_keyvalue=False, include_null=True):
    result = []
    for raw_item in raw_result:
        item = dict() if not as_keyvalue else []
        for key, value in raw_item.items():
            if not include_null and key.startswith("!"):
                continue
            
            key = key[1:] if key.startswith("!") else key
            if as_keyvalue:
                is_null = False if value else True
                item.append({
                    KEY_NAME: key, 
                    KEY_VALUE: value, 
                    KEY_ISNULL: is_null
                })
            else:
                item[key] = value

        result.append(item)

    return result

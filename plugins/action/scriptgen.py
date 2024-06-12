#!/usr/bin/python

from ansible.utils.display import Display
from typing import Dict
from enum import Enum

from ansible.module_utils.basic import *
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleAction, _AnsibleActionDone, AnsibleActionFail, AnsibleActionSkip
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import cmd_spec

display = Display()


def get_argument_spec():
    argument_spec = dict(
        commands=cmd_spec.get_spec(True)
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

        commands = new_module_args[cmd_spec.KEY_COMMANDS]

        output = self.process(commands, task_vars)
        return output


    def process(self, commands, task_vars):
        rsc_script = cmd_spec.commands_to_script(commands)

        display.debug("Generated script: %s" % rsc_script)

        output = {
            "failed": False,
            "changed": False,
            "input": commands,
            "script": rsc_script,
        }
        return output


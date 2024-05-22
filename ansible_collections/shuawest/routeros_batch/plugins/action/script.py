#!/usr/bin/python

from ansible.utils.display import Display
from typing import Dict
from enum import Enum

from ansible.errors import AnsibleError, AnsibleAction, _AnsibleActionDone, AnsibleActionFail, AnsibleActionSkip
from ansible.plugins.action import ActionBase
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import cmd_spec

display = Display()


SCRIPT_PATH = "/system script"
REMOVE_FAILED_MSG = "no such item"

KEY_CHANGED = "changed"
KEY_FAILED = "failed"
KEY_MSG = "msg"

KEY_CLEAN_MSG = "clean_msg"
KEY_REPLACED = "replaced_script"
KEY_REPLACED_MSG = "replaced_msg"

CTX_ADD = "add_result"
CTX_REMOVE = "remove_result"
CTX_CLEAN = "clean_result"
CTX_EXEC = "exec_result"

class ScriptAction(Enum):
    ADD = "add"
    RUN = "run"
    REMOVE = "remove"

class ScriptState(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXECUTED = "executed"
    EXECUTED_ONCE = "executed_once"
    EXECUTED_CLEAN = "executed_clean"

def get_argument_spec():
    # routeros vars from https://docs.ansible.com/ansible/latest/collections/community/routeros/api_module.html
    argument_spec = dict(
        name=dict(type='str', required=True),
        comment=dict(type='str', required=False),
        verbose_steps=dict(type='bool', default=False),
        state=dict(type='str', required=True, choices=[
            ScriptState.PRESENT.value, 
            ScriptState.ABSENT.value, 
            ScriptState.EXECUTED.value, 
            ScriptState.EXECUTED_ONCE.value, 
            ScriptState.EXECUTED_CLEAN.value]),
        content=dict(type='str', required=False),
        commands=cmd_spec.get_spec(False),
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
        routeros_vars = module_args["routeros"]

        name = module_args["name"]
        comment = module_args["comment"]
        state = module_args["state"]
        content = module_args["content"]
        commands = module_args["commands"]
        verbose_steps = module_args["verbose_steps"]

        # determine the script content
        rsc_script = ""
        is_commands = False
        if not content and not commands:
            raise AnsibleActionFail("Either content or commands must be provided")
        elif content and commands:
            raise AnsibleActionFail("Either content or commands must be provided, not both")
        elif content:
            rsc_script = content
        elif commands:
            is_commands = True
            rsc_script = cmd_spec.commands_to_script(commands)
        else: 
            raise AnsibleActionFail("Invalid state")

        
        # process the script based on the state argument
        context = {}
        if state == ScriptState.PRESENT.value: 
            context[CTX_REMOVE] = self.remove_script(task_vars, routeros_vars, name, False)
            context[CTX_ADD] = self.add_script(task_vars, routeros_vars, name, rsc_script, comment)
        
        elif state == ScriptState.ABSENT.value:
            context[CTX_REMOVE] = self.remove_script(task_vars, routeros_vars, name, False)
            
        elif state == ScriptState.EXECUTED.value:
            context[CTX_EXEC] = self.exec_script(task_vars, routeros_vars, name)
  
        elif state == ScriptState.EXECUTED_ONCE.value:
            context[CTX_REMOVE] = self.remove_script(task_vars, routeros_vars, name, False)
            context[CTX_ADD] = self.add_script(task_vars, routeros_vars, name, rsc_script, comment)
            # only run if add was successful
            if not _step_failed(context, CTX_ADD):
                context[CTX_EXEC] = self.exec_script(task_vars, routeros_vars, name)
            
        elif state == ScriptState.EXECUTED_CLEAN.value:
            context[CTX_REMOVE] = self.remove_script(task_vars, routeros_vars, name, False)
            context[CTX_ADD] = self.add_script(task_vars, routeros_vars, name, rsc_script, comment)
            # only run if add was successful
            if not _step_failed(context, CTX_ADD):
                context[CTX_EXEC] = self.exec_script(task_vars, routeros_vars, name)
                context[CTX_CLEAN] = self.remove_script(task_vars, routeros_vars, name, False)
             
        else: 
            raise AnsibleActionFail("Invalid state '{}'".format(state))

        # process the context to output
        output = _process_script_output(context, name, state, rsc_script, is_commands, verbose_steps)
        
        return output


    def add_script(self, sys_vars, routeros_vars, name, rsc_script, comment):
        api_add_args = _prepare_routeros_args(dict(name=name, 
                         source=rsc_script,
                         comment=comment))
        add_result = self.add_script_by_args(sys_vars, routeros_vars, api_add_args)
        return add_result

    def add_script_by_args(self, sys_vars, routeros_vars, str_args):
        add_result = self.exec_routeros_api(sys_vars, routeros_vars, SCRIPT_PATH, ScriptAction.ADD.value, str_args)
        return add_result
               

    def remove_script(self, sys_vars, routeros_vars, name, must_exist=False):
        remove_result = self.exec_routeros_api(sys_vars, routeros_vars, SCRIPT_PATH, ScriptAction.REMOVE.value, name)
        
        if must_exist and remove_result["msg"] == REMOVE_FAILED_MSG:
            raise AnsibleActionFail("Failed to remove script '{}'".format(name))
        
        return remove_result


    def exec_script(self, sys_vars, routeros_vars, name):
        run_args = "run number=%s" % name
        exec_result = self.exec_routeros_api(sys_vars, routeros_vars, SCRIPT_PATH, "cmd", run_args)
        return exec_result
    

    def exec_routeros_api(self, sys_vars, routeros_vars, path, action, action_args):
        api_args = dict(**routeros_vars)
        api_args["path"] = path
        api_args[action] = action_args

        api_result = self._execute_module(
            module_name='community.routeros.api', 
            module_args=api_args, 
            task_vars=sys_vars)

        return api_result


def _prepare_routeros_args(args: Dict):
    ros_kvargs = ""
    for key, value in args.items():
        ros_kvargs += f"{key}=\"{value}\" "
    return ros_kvargs

    
# Process context to formatted output
# - process and condense output for return
# - error checking and handling, determining changed & failed flags
# TODO: determine how to catpure the script output & logs
def _process_script_output(context, name, state, rsc_script, is_commands=False, verbose_steps=False):
    changed = False
    failed = False

    # initialize output
    output = dict({"name": name, "state": state, "script": rsc_script})

    # determine if script was replaced, for any state other than 'absent'
    if state != ScriptState.ABSENT.value:
        remove_changed = _step_changed(context, CTX_REMOVE)
        add_changed = _step_changed(context, CTX_ADD)
        changed = _step_changed(context, CTX_REMOVE) or _step_changed(context, CTX_ADD)     
        remove_msg = _step_msg(context, CTX_REMOVE)
        add_msg = _step_msg(context, CTX_ADD)
        if remove_changed and add_changed:
            output[KEY_REPLACED] = True
            output[KEY_REPLACED_MSG] = "Script '%s' was replaced: %s; %s" % (name, remove_msg, add_msg)
        elif not remove_changed and add_changed:
            output[KEY_REPLACED] = True
            output[KEY_REPLACED_MSG] = "Script '%s' was added, a script with the same name was not present prior: %s" % (name, add_msg)
        elif remove_changed and not add_changed:
            output[KEY_REPLACED] = False
            output[KEY_REPLACED_MSG] = "Script '%s' was partially replaced. It was removed but failed to add during replace.\nremoved: %s\nadded: %s" % (name, remove_msg, add_msg)
        else:
            output[KEY_REPLACED] = False
            output[KEY_REPLACED_MSG] = "Script %s was not on device" % name

        # add result    
        add_failed = _step_failed(context, CTX_ADD)
        if add_failed:
            failed = True
            add_err_msg = _step_msg(context, CTX_ADD)
            output[KEY_MSG] = "Failed to add script '%s': %s" % (name, add_err_msg)

        # exec result
        executed_states = [ScriptState.EXECUTED.value, ScriptState.EXECUTED_ONCE.value, ScriptState.EXECUTED_CLEAN.value]
        if not add_failed and state in executed_states:
            exec_failed = _step_failed(context, CTX_EXEC)
            if exec_failed: 
                failed = True
                script_err_message = _step_msg(context, CTX_EXEC)
                if is_commands:  
                    output[KEY_MSG] = "Failed to execute script '%s' generated from commands. Review the generated script, checking the attribute names and values are correct. Error: %s" % (name, script_err_message)
                else:
                    output[KEY_MSG] = "Failed to execute content in '%s' script: %s" % (name, script_err_message)
            else:
                changed = True
                output[KEY_MSG] = "Executed script '%s'" % name

            # clean result
            if state == ScriptState.EXECUTED_CLEAN.value: 
                clean_failed = _step_failed(context, CTX_CLEAN)
                if clean_failed or failed: 
                    failed = True
                    script_err_message = _step_msg(context, CTX_CLEAN)
                    output[KEY_CLEAN_MSG] = "Failed to clean up script '%s' after execution. Review the script and device for any issues. Error: %s" % (name, script_err_message)
                else:
                    changed = True
                    output[KEY_CLEAN_MSG] = "Removed script '%s' after execution" % name

    # set the final negotiation flags
    output[KEY_FAILED] = failed
    output[KEY_CHANGED] = changed

    # add full context for remove, add, exec, clean to output
    if verbose_steps:
        if CTX_REMOVE in context:
            output[CTX_REMOVE] = context[CTX_REMOVE]
        if CTX_ADD in context:
            output[CTX_ADD] = context[CTX_ADD]
        if CTX_EXEC in context:
            output[CTX_EXEC] = context[CTX_EXEC]  
        if CTX_CLEAN in context:
            output[CTX_CLEAN] = context[CTX_CLEAN]   

    return output

def _step_changed(context, ctx_key):
    if ctx_key in context:
        ctx = context[ctx_key]
        if KEY_CHANGED in ctx:
            return ctx[KEY_CHANGED]
    return False

def _step_failed(context, ctx_key):
    if ctx_key in context:
        ctx = context[ctx_key]
        if KEY_FAILED in ctx:
            return ctx[KEY_FAILED]
    return False

def _step_msg(context, ctx_key):
    if ctx_key in context:
        ctx = context[ctx_key]
        if KEY_MSG in ctx:
            return ctx[KEY_MSG]
    return ""

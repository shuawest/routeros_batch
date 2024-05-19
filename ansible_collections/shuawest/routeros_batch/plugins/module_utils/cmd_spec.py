# from __future__ import absolute_import, division, print_function
# __metaclass__ = type
# from typing import Dict
from enum import Enum

# from ansible.errors import AnsibleError #, AnsibleAction, _AnsibleActionDone, AnsibleActionFail, AnsibleActionSkip
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import ros_paths


class PathType(Enum):
    LOOKUP = "lookup"
    LIST = "list"
    ITEM = "item"

class ValueMode(Enum):
    SET = "set"
    MATCH = "match"
    BOTH = "both"

class CommandState(Enum):
    PRESENT = "present"
    ABSENT = "absent"

KEY_COMMANDS = "commands"
KEY_DESC = "desc"
KEY_STATE = "state"
KEY_MODE = "mode"
KEY_VALUES = "values"

KEY_PATH_TYPE = "path_type"
KEY_PATH = "path"
KEY_ATTR = "attr"
KEY_VALUE = "value"


def get_routeros_spec():
    routeros=dict(type='dict', required=True, options={
        'username': dict(type='str', required=True),
        'password': dict(type='str', required=True, no_log=True),
        'hostname': dict(type='str', required=True),
        'port': dict(type='int'),
        'tls': dict(type='bool', default=False, aliases=['ssl']),
        'force_no_cert': dict(type='bool', default=False),
        'validate_certs': dict(type='bool', default=True),
        'validate_cert_hostname': dict(type='bool', default=False),
        'ca_path': dict(type='path'),
        'encoding': dict(type='str', default='ASCII'),
        'timeout': dict(type='int', default=10),
    })
    return routeros

def get_spec(is_commands_required=False):
    commands=dict(type='list', elements='dict', required=is_commands_required, options={
            KEY_DESC: dict(type='str', required=True),
            KEY_PATH: dict(type='str', required=True),
            KEY_PATH_TYPE: dict(type='str', choices=[
                PathType.LOOKUP.value, 
                PathType.LIST.value, 
                PathType.ITEM.value,], default=PathType.LOOKUP.value),
            KEY_STATE: dict(type='str', choices=[
                CommandState.PRESENT.value, 
                CommandState.ABSENT.value], default=CommandState.PRESENT.value),
            KEY_VALUES: dict(type='list', elements='dict', options={
                KEY_ATTR: dict(type='str', required=True),
                KEY_VALUE: dict(type='str', required=True),
                KEY_MODE: dict(type='str', choices=[
                    ValueMode.SET.value, 
                    ValueMode.MATCH.value, 
                    ValueMode.BOTH.value], default=ValueMode.SET.value),
            }),
        },
    )
    return commands


def commands_to_script(commands):
    rsc_script = ""
    for command in commands:
        cmd_script = command_to_script(command)
        rsc_script += cmd_script + "\n\n"
    return rsc_script

def command_to_script(command):
    script = "; ### %s: %s ### ;\n\n" % (command[KEY_STATE], command[KEY_DESC])

    path_type = command[KEY_PATH_TYPE]
    if path_type == PathType.LOOKUP.value:
        path = command[KEY_PATH]
        if path in ros_paths.ROUTEROS_ITEM_PATHS or "/"+path in ros_paths.ROUTEROS_ITEM_PATHS:
            script += item_command_to_script(command)
        elif path in ros_paths.ROUTEROS_LIST_PATHS or "/"+path in ros_paths.ROUTEROS_LIST_PATHS:
            script += list_command_to_script(command)
        else:
            raise Exception("Unrecognized path: path '%s' is not recognized as a item or list path in the lookup. Check that the path is correct. If it is correct, then set the command path_type to 'item' or 'list'." % path)
    elif path_type == PathType.ITEM.value:
        script += item_command_to_script(command)
    elif path_type == PathType.LIST.value:
        script += list_command_to_script(command)

    return script

def item_command_to_script(command):
    value_keypairs = command_value_keypairs(command)
    script = "%s set %s" % (command[KEY_PATH], value_keypairs)
    return script

def list_command_to_script(command):
    match_keypairs = command_match_keypairs(command)
    value_keypairs = command_value_keypairs(command)

    if command[KEY_STATE] == CommandState.PRESENT.value:   
        script = ":if ([:len [%s find %s]] > 0) do={\n" % (command[KEY_PATH], match_keypairs)
        script += "\t%s set [ find %s] %s\n" % (command[KEY_PATH], match_keypairs, value_keypairs)
        script += "} else={\n"
        script += "\t%s add %s\n" % (command[KEY_PATH], value_keypairs)
        script += "}\n"

    if command[KEY_STATE] == CommandState.ABSENT.value:
        script = ":if ([:len [%s find %s]] > 0) do={\n" % (command[KEY_PATH], match_keypairs)
        script += "\t%s remove [ find %s]\n" % (command[KEY_PATH], match_keypairs)
        script += "}\n"

    return script

def command_value_keypairs(command):
    keypairs = ""
    for value in command[KEY_VALUES]:
        if value[KEY_MODE] == ValueMode.SET.value or value[KEY_MODE] == ValueMode.BOTH.value:
            val = format_value(value[KEY_VALUE])
            keypairs += "%s=%s " % (value[KEY_ATTR], val)
    return keypairs

def command_match_keypairs(command):
    keypairs = ""
    for value in command[KEY_VALUES]:
        if value[KEY_MODE] == ValueMode.MATCH.value or value[KEY_MODE] == ValueMode.BOTH.value:
            val = format_value(value[KEY_VALUE])
            keypairs += "%s=%s " % (value[KEY_ATTR], val)
    return keypairs

def format_value(value):
    if value == "True":
        return "yes"
    elif value == "False":
        return "no"
    else: 
        return "\\\"" + value + "\\\""



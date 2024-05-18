from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.shuawest.routeros_batch.tests.unit.compat.mock import patch
from ansible_collections.shuawest.routeros_batch.tests.unit.plugins.modules.utils import set_module_args

from ansible_collections.shuawest.routeros_batch.plugins.module_utils import cmd_spec
from ansible_collections.shuawest.routeros_batch.plugins.module_utils import ros_paths

import unittest
import logging
import sys
import yaml
import os


class TestActionBase(unittest.TestCase):
        
    def test_scriptgen_example(self):
        logging.info("scriptgen test_scriptgen_example")
        with open('tests/unit/data/mtk-base.yaml', 'r') as file:
            commands = yaml.safe_load(file)

        result = cmd_spec.commands_to_script(commands)

        logging.info("scriptgen result: %s", result)
        self.dump_to_yaml(result, 'scriptgen-example-result.yaml')
        self.dump_to_file(result['script'], 'scriptgen-example-result.rsc')


    def test_scriptgen_simple(self):
        logging.info("scriptgen test_scriptgen_simple")
        with open('tests/unit/data/commands-simple.yaml', 'r') as file:
            commands = yaml.safe_load(file)

        result = cmd_spec.commands_to_script(commands)

        self.dump_to_yaml(result, 'scriptgen-simple-result.yaml')
        self.dump_to_file(result['script'], 'scriptgen-simple-result.rsc')

        logging.info("scriptgen result: %s", result)
        commandA = result['meta']['input'][0]
        self.assertEqual(commandA['desc'], 'command A')
        self.assertEqual(commandA['path'], 'interface bridge')
        self.assertEqual(commandA['state'], 'present')
        self.assertEqual(commandA['values'][0]['attr'], 'name')
        self.assertEqual(commandA['values'][0]['value'], 'bridge1')
        self.assertEqual(commandA['values'][0]['mode'], 'both')
        self.assertEqual(commandA['values'][1]['attr'], 'fast-forward')
        self.assertEqual(commandA['values'][1]['value'], 'False')
        self.assertEqual(commandA['values'][1]['mode'], 'set')
        commandB = result['meta']['input'][1]
        self.assertEqual(commandB['desc'], 'command B')
        self.assertEqual(commandB['path'], 'interface bridge port')
        self.assertEqual(commandB['state'], 'absent')
        self.assertEqual(commandB['values'][0]['attr'], 'bridge')
        self.assertEqual(commandB['values'][0]['value'], 'bridge1')
        self.assertEqual(commandB['values'][0]['mode'], 'both')
        self.assertEqual(commandB['values'][1]['attr'], 'interface')
        self.assertEqual(commandB['values'][1]['value'], 'interfaceA')
        self.assertEqual(commandB['values'][1]['mode'], 'both')
        self.assertEqual(commandB['values'][2]['attr'], 'hw')
        self.assertEqual(commandB['values'][2]['value'], 'False')
        self.assertEqual(commandB['values'][2]['mode'], 'set')

    def test_get_argument_spec(self):
        argspec = cmd_spec.get_spec()
        # display.debug("argument_spec: %s" % argspec)
        #assert argspec.commands.elements.desc.required == True  # doesn't work - would need to parse
        assert argspec['commands']['options']['desc']['required'] == True


    def dump_to_yaml(self, data, filename):
        # Write commands to a file in /tmp
        with open(os.path.join('/tmp', filename), 'w') as file:
            yaml.dump(data, file)

    def dump_to_file(self, content, filename):
        # Write commands to a file in /tmp
        with open(os.path.join('/tmp', filename), 'w') as file:
            file.write(content)


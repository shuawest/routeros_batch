#!/usr/bin/python

DOCUMENTATION = '''
---
module: scriptgen
author: 
- Josh West (@shuawest)
short_description: Generate Mikrotik RouterOS script to modify configuration with idempotent configuration
version_added: "0.1"
description:
  - Generates a routeros script to reconcile configuration objects and parameters using a set of command objects.
extends_documentation_fragment: []
attributes:
  platform:
    platforms: RouterOS
options:
  commands:
    description:
      - List of commands to generate script
    required: true
    type: list
    elements: dict
    suboptions:
      desc:
        description:
          - Description of the command
        required: true
        type: str
      path:
        description:
          - Full path to the configuration object
        required: true
        type: str
      state:
        description:
          - State of the configuration object
        required: true
        default: "present"
        type: str
        choices: [ "present", "absent" ]
      values:
        description:
          - List of key-value pairs to set on the configuration object
        required: false
        type: list
        elements: dict
        suboptions:
          attr:
            description:
              - Attribute name
            required: true
            type: str
          value:
            description:
              - Value to set
            required: true
            type: str
          mode:
            description:
              - Mode to use for this attribute value in the script
              - V(set) will set the value only
              - V(match) will query for matching objects using this value
              - V(both) will both query with the value and set the value
              - V(clear) will set the value to null 
              - if changing a value you are querying based on, use the same attribute name with the old value using V(match) and new value using V(set)
            required: false
            default: "set"
            type: str
            choices: [ "set", "match", "both", "clear" ]
seealso:
  - module: community.routeros.api
'''


EXAMPLES = '''
- name: Add a bridge
  routeros_batch.scriptgen:
    commands: 
    - desc: 'Put VPN bridge'
      path: '/interface bridge'
      state: present
      values:
      - attr: 'name'
        value: 'bridge1'
        mode: both
      - attr: 'fast-forward'
        value: 'False'
        mode: set
    - desc: 'Add a bridge port'
      path: '/interface bridge port'
      state: present
      values:
      - attr: 'bridge'
        value: 'bridge1'
        mode: both
  register: result

- name: Remove a bridge
  routeros_batch.scriptgen:
    commands: 
    - desc: 'Remove a bridge port'
      path: '/interface bridge port'
      state: absent
      values:
      - attr: 'bridge'
        value: 'bridge1'
        mode: both
    - desc: 'Remove VPN bridge'
      path: '/interface bridge'
      state: absent
      values:
      - attr: 'name'
        value: 'bridge1'
        mode: both
      - attr: 'fast-forward'
        value: 'False'
        mode: set
  register: result

- name: Change a bridge name
  routeros_batch.scriptgen:
    commands: 
    - desc: 'Change bridge name bridge'
      path: '/interface bridge'
      state: present
      values:
      - attr: 'name'
        value: 'bridgeOld'
        mode: match
      - attr: 'name'
        value: 'bridgeNew'
        mode: set
  register: result
'''

RETURN = '''
---
script:
  description: Generate rsc script content
  type: string
  returned: always
  sample: 
  - | 
      ; ### present: Put VPN bridge 'bridge1' ### ;

      :if ([:len [/interface bridge find name=bridge1 ]] > 0) do={
              /interface bridge set [ find name=bridge1 ] name=bridge fast-forward=no 
      } else={
              /interface bridge add name=bridge1 fast-forward=no 
      }
'''

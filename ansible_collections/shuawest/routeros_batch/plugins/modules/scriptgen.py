#!/usr/bin/python

DOCUMENTATION = '''
---
module: scriptgen
short_description: Generate Mikrotik RouterOS idempotent script   
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
'''

RETURN = '''
"result": {
    "changed": true,
    "failed": false,
    "meta": {
        "input": [...],
        "script": "
            ; ### present: Put VPN bridge 'bridge1' ### ;

            :if ([:len [/interface bridge find name=bridge1 ]] > 0) do={
                    /interface bridge set [ find name=bridge1 ] name=bridge fast-forward=no 
            } else={
                    /interface bridge add name=bridge1 fast-forward=no 
            }
        "
    }
}
'''

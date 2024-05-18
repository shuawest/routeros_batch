#!/usr/bin/python

DOCUMENTATION = '''
---
module: routeros_batch.script
short_description: Add, remove, execute a named script on a Mikrotik RouterOS device
'''

EXAMPLES = '''
- name: Run a set of commands converted to a routeros script on a Mikrotik device
  routeros_batch.script: 
    name: "ros_cmd_script1"
    comment: "added by ansible" 
    state: executed_once        # add/replace script, run, and leave it on the device
    routeros:
      username: "{{ routeros_user }}"
      password: "{{ routeros_pass }}"
      hostname: "{{ routeros_host }}"
    commands: 
    - desc: Put VPN bridge 'bridge'
      path: /interface bridge
      state: present
      values:
      - attr: name
        value: bridge
        mode: both
      - attr: fast-forward
        value: no
    - desc: VPN user 'guest'
      path: /ppp secret
      state: present            # add/update user
      values:
      - attr: name
        value: guest
        mode: both
      - attr: password
        value: "{{ guest_pass }}"
      - attr: profile
        value: profile-vpn
      - attr: service
        value: any
  register: ros_cmd_script1_result

- name: Run a script as content against Mikrotik RouterOS
  routeros_batch.script: 
    name: "ros_content_script2"
    comment: "added by ansible rosapi integration test" 
    state: executed_clean        # add/replace script, run, then remove it from the device
    routeros:
      username: "{{ routeros_user }}"
      password: "{{ routeros_pass }}"
      hostname: "{{ routeros_host }}"
    content: |
      /system identity print
      /system resource print
  register: ros_content_script1_result  

- name: Remove a script by name from a Mikrotik RouterOS
  routeros_batch.script: 
    name: "old_script_a"
    state: absent        # remove script
    routeros:
      username: "{{ routeros_user }}"
      password: "{{ routeros_pass }}"
      hostname: "{{ routeros_host }}"
  register: ros_remove_result  

'''

RETURN = '''
"script_command_int_test": {
    "changed": true,
    "clean_msg": "Executed script 'script_command_int_test' and cleaned up",
    "failed": false,
    "msg": "Executed script 'script_command_int_test'",
    "name": "script_command_int_test",
    "replaced_msg": "Script 'script_command_int_test' was added, a script with the same name was not present prior: ['added: .id= *21']",
    "replaced_script": true,
    "script": "; ### present: Put VPN bridge 'bridge' ### ;\n\n:if ([:len [/interface bridge find name=\\\"bridge\\\" ]] > 0) do={\n\t/interface bridge set [ find name=\\\"bridge\\\" ] name=\\\"bridge\\\" fast-forward=no \n} else={\n\t/interface bridge add name=\\\"bridge\\\" fast-forward=no \n}\n\n\n; ### absent: Remove VPN user 'guest' ### ;\n\n:if ([:len [/ppp secret find name=\\\"guest\\\" ]] > 0) do={\n\t/ppp secret remove [ find name=\\\"guest\\\" ]\n}\n\n\n",
    "state": "executed_clean"
}

"bad_attribute_int_test": {
    "changed": true,
    "clean_msg": "Executed script 'bad_attribute_int_test' and cleaned up",
    "failed": true,
    "msg": "Failed to execute script 'bad_attribute_int_test' generated from commands. Review the generated script, checking the attribute names and values are correct. Error: ['expected end of command (line 4 column 58)']",
    "name": "bad_attribute_int_test",
    "replaced_msg": "Script 'bad_attribute_int_test' was added, a script with the same name was not present prior: ['added: .id= *22']",
    "replaced_script": true,
    "script": "; ### present: Put VPN bridge 'bridge' ### ;\n\n:if ([:len [/interface bridge find fake_attr=\\\"bridge\\\" ]] > 0) do={\n\t/interface bridge set [ find fake_attr=\\\"bridge\\\" ] fake_attr=\\\"bridge\\\" fast-forward=no \n} else={\n\t/interface bridge add fake_attr=\\\"bridge\\\" fast-forward=no \n}\n\n\n",
    "state": "executed_clean"
}
'''  


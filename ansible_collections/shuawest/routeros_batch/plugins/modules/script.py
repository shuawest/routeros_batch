#!/usr/bin/python

DOCUMENTATION = '''
---
module: routeros_batch.script
author: 
- Josh West (@shuawest)
short_description: Add, remove, execute a named script on a Mikrotik RouterOS device
description: 
- The script can be added, removed, executed, executed once, or executed and removed from the device
- Uses the community.routeros.api module to interact with the Mikrotik RouterOS API
- C(routeros) provides the connection details to the device following the community.routeros.api module paramters
notes:
- Use `content` to update a script with direct content or a variable
- Use `commands` to generate a script from a list of commands and apply it to a device
- Currently the script output cannot be captured or logged during script execution
- This is an action module that calls multiple apis to add, remove, and execute scripts. Use the `verbose_steps` flag to see the result of each individual step output.
attributes:
  platform:
    platforms: RouterOS
options:
  name:
    description:
      - Name of the script to add, remove, or execute
    required: true
    type: str
  comment:
    description:
      - Comment to add to the script
    required: false
    type: str
  verbose_steps:
    description:
      - Show the result of each individual step in the output
    required: false
    type: bool
  state:
    description:
      - State of the script for the task execution
    required: true
    type: str
    choices: [ "present", "absent", "executed", "executed_once", "executed_clean" ]
  content:
    description:
      - Direct content to add to the script
      - Mutually exclusive with O(commands)
    required: false
    type: str
  commands:
    description:
      - List of commands to generate script
      - Mutually exclusive with O(content)
    required: false
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
              - Refer to the routeros_batch.scriptgen module for more information
  routeros:
    description:
      - Connection details to the Mikrotik RouterOS device
      - Refer to the community.routeros.api module parameters for more information
    required: true
    type: dict
    suboptions:
      hostname:
        description:
          - Hostname or IP address of the RouterOS device
        required: true
        type: str
      username:
        description:
          - Username to authenticate with
        required: true
        type: str
      password:
        description:
          - Password to authenticate with
        required: true
        type: str
seealso:
  - module: community.routeros.api
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
name: 
  description: Name of the script
  type: string
  returned: always
  sample:
  - "myscript"
msg:
  description: Generate rsc script content
  type: string
  returned: always
  sample: 
  - "Executed script 'myscript'"
script:
  description: RouterOS script content
  type: string
  returned: always
  sample:
  - "; ### present: Put VPN bridge 'bridge' ### ;\n\n:if ([:len [/interface bridge find name=\\\"bridge\\\" ]] > 0) do={\n\t/interface bridge set [ find name=\\\"bridge\\\" ] name=\\\"bridge\\\" fast-forward=no \n} else={\n\t/interface bridge add name=\\\"bridge\\\" fast-forward=no \n}\n\n\n; ### absent: Remove VPN user 'guest' ### ;\n\n:if ([:len [/ppp secret find name=\\\"guest\\\" ]] > 0) do={\n\t/ppp secret remove [ find name=\\\"guest\\\" ]\n}\n\n\n",
state:
  description: State of the script for the task execution
  type: string
  returned: always
  sample:
  - "executed_clean"
replaced_script:
  description: Whether the script was replaced
  type: bool
  returned: always
  sample:
  - true
replaced_msg:
  description: Message indicating if the script was replaced
  type: string
  returned: always
  sample:
  - "Script 'myscript' was added, a script with the same name was not present prior: ['added: .id= *21']"
clean_msg:
  description: Message indicating the script was cleaned up
  type: string
  returned: always
  sample:
  - "Executed script 'myscript' and cleaned up"
'''  


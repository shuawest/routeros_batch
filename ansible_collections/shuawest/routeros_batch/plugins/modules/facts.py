#!/usr/bin/python

DOCUMENTATION = '''
---
module: routeros_batch.facts
author: 
- Josh West (@shuawest)
short_description: Fetch facts with a list of paths using the Mikrotik RouterOS api
description: 
- Batch fetch facts from the device using a list of paths
- Uses the C(community.routeros.api_facts) module to interact with the Mikrotik RouterOS API
- C(routeros) provides the connection details to the device following the C(community.routeros.api_facts) module paramters
notes:
- Use O(paths) to fetch facts from the device using a list of paths
- For list objects it pulls all objects and attributes without a filter
- Be aware of the amount of data being pulled from the device - use the C(routeros.api_facts) module if more precision is required.
attributes:
  platform:
    platforms: RouterOS
options:
  paths:
    description:
      - List of paths to fetch facts from the device
    required: true
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Name of the variable to set in the output dictionary of values for the RouterOS object
        required: true
        type: str
      path:
        description:
          - Path to the object to fetch
        required: true
        type: str
  as_keyvalue:
    description:
      - Return the facts as a key-value pairs, instead of dictionaries
    required: false
    type: bool
    default: false
  include_null:
    description:
      - Include null values in the output
    required: false
    type: bool
    default: true
  routeros:
    description:
      - Connection details to the device
      - Refer to the C(community.routeros.api) module parameters for more information
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
          - Username to use for the connection
        required: true
        type: str
      password:
        description:
          - Password to use for the connection
        required: true
        type: str
seealso:
  - module: community.routeros.api_facts
'''


EXAMPLES = '''
- name: Batch fetch RouterOS facts for the VPN configuration
  routeros_batch.facts: 
    routeros:
      username: "{{ routeros_user }}"
      password: "{{ routeros_pass }}"
      hostname: "{{ routeros_host }}"
    paths: 
      - name: bridges       
        path: interface bridge
      - name: bridge_ports       
        path: interface bridge port
      - name: dhcp_clients      
        path: ip dhcp-client
      - name: ips
        path: ip address
      - name: ip_pools       
        path: ip pool
      - name: firewall_filters      
        path: ip firewall filter
      - name: firewall_nats      
        path: ip firewall nat
      - name: ipsec_identities      
        path: ip ipsec identity
      - name: ipsec_peers       
        path: ip ipsec peer
      - name: ipsec_proposal       
        path: ip ipsec proposal
      - name: ipsec_settings      
        path: ip ipsec settings
      - name: l2tp_server      
        path: interface l2tp-server server
      - name: ppp_profiles      
        path: ppp profile
  register: ros_facts_result
'''

RETURN = '''
"<name>": 
  description: Name of the of the path
  type: list
  elements: dict
  returned: always
  suboptions:
    path:
      description: Path to the object
      type: str
    path_type:
      description: Describes the single versus list type of the path
      type: str
    values:
      description: List of objects and their attribute values
      type: list
      elements: dict
      suboptions:
        name:
          description: Attribute value
          type: str
        value:
          description: Value of the attribute
          type: str
        is_null:
          description: Indicates if the value is null
          type: bool
'''  


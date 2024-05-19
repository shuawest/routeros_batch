#!/usr/bin/python

DOCUMENTATION = '''
---
module: routeros_batch.facts
short_description: Fetch facts with a list of paths using the Mikrotik RouterOS api
'''

EXAMPLES = '''
- name: Batch fetch RouterOS facts
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
"ros_facts_result": {

}

"failed_bad_path_facts_result": {

}

'''  


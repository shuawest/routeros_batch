import array

ROUTEROS_LIST_PATHS = [
	'/ppp profile',
	'/ppp secret',
	'/ip ipsec mode-config',
	'/caps-man access-list',
	'/caps-man channel',
	'/caps-man configuration',
	'/caps-man datapath',
	'/caps-man manager interface',
	'/caps-man provisioning',
	'/caps-man security',
	'/interface bonding',
	'/interface bridge',
	'/interface bridge port',
	'/interface bridge vlan',
	'/interface eoip',
	'/interface gre',
	'/interface gre6',
	'/interface list',
	'/interface list member',
	'/interface pppoe-client',
	'/interface vlan',
	'/interface vrrp',
	'/interface wireguard',
	'/interface wireguard peers',
	'/ip address',
	'/ip arp',
	'/ip dhcp-client',
	'/ip dhcp-client option',
	'/ip dhcp-server',
	'/ip dhcp-server lease',
	'/ip dhcp-server network',
	'/ip dns static',
	'/ip firewall address-list',
	'/ip firewall filter',
	'/ip firewall layer7-protocol',
	'/ip firewall mangle',
	'/ip firewall nat',
	'/ip firewall raw',
	'/ip ipsec identity',
	'/ip ipsec peer',
	'/ip ipsec policy',
	'/ip ipsec profile',
	'/ip ipsec proposal',
	'/ip pool',
	'/ip route',
	'/ip traffic-flow target',
	'/ipv6 address',
	'/ipv6 dhcp-client',
	'/ipv6 dhcp-server',
	'/ipv6 dhcp-server option',
	'/ipv6 firewall address-list',
	'/ipv6 firewall filter',
	'/ipv6 firewall mangle',
	'/ipv6 firewall raw',
	'/ipv6 nd',
	'/ipv6 route',
	'/mpls ldp',
	'/queue tree',
	'/routing ospf area',
	'/routing ospf area range',
	'/routing ospf instance',
	'/routing ospf interface-template',
	'/routing pimsm instance',
	'/routing pimsm interface-template',
	'/snmp community',
	'/system logging',
	'/system logging action',
	'/system ntp client servers',
	'/system scheduler',
	'/system script',
	'/user group'
]

ROUTEROS_ITEM_PATHS = [
	'/caps-man aaa',
	'/caps-man manager',
	'/certificate settings',
	'/interface bridge mlag',
	'/interface bridge port-controller',
	'/interface bridge port-extender',
	'/interface bridge settings',
	'/interface detect-internet',
	'/interface ethernet',
	'/interface ethernet poe',
	'/interface ethernet switch',
	'/interface ethernet switch port',
	'/interface l2tp-server server',
	'/interface ovpn-server server',
	'/interface pptp-server server',
	'/interface sstp-server server',
	'/interface wireless align',
	'/interface wireless cap',
	'/interface wireless sniffer',
	'/interface wireless snooper',
	'/ip accounting',
	'/ip accounting web-access',
	'/ip cloud',
	'/ip cloud advanced',
	'/ip dhcp-server config',
	'/ip dns',
	'/ip firewall connection tracking',
	'/ip firewall service-port',
	'/ip hotspot service-port',
	'/ip ipsec settings',
	'/ip neighbor discovery-settings',
	'/ip proxy',
	'/ip route vrf',
	'/ip service',
	'/ip settings',
	'/ip smb',
	'/ip socks',
	'/ip ssh',
	'/ip tftp settings',
	'/ip traffic-flow',
	'/ip traffic-flow ipfix',
	'/ip upnp',
	'/ipv6 nd prefix default',
	'/ipv6 settings',
	'/mpls',
	'/port firmware',
	'/ppp aaa',
	'/queue interface',
	'/radius incoming',
	'/routing bgp instance',
	'/routing mme',
	'/routing rip',
	'/routing ripng',
	'/snmp',
	'/system clock',
	'/system clock manual',
	'/system identity',
	'/system leds settings',
	'/system note',
	'/system ntp client',
	'/system ntp server',
	'/system package update',
	'/system routerboard settings',
	'/system upgrade mirror',
	'/system watchdog',
	'/tool bandwidth-server',
	'/tool e-mail',
	'/tool graphing',
	'/tool mac-server',
	'/tool mac-server mac-winbox',
	'/tool mac-server ping',
	'/tool romon',
	'/tool sms',
	'/tool sniffer',
	'/tool traffic-generator'
]



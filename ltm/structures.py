class VirtualServerType:
	RESOURCE_TYPE_POOL = 0
	RESOURCE_TYPE_IP_FORWARDING = 1
	RESOURCE_TYPE_L2_FORWARDING = 2
	RESOURCE_TYPE_REJECT = 3
	RESOURCE_TYPE_FAST_L4 = 4
	RESOURCE_TYPE_FAST_HTTP = 5
	RESOURCE_TYPE_STATELESS = 6
	
	RESOURCE_TYPES = (
		'Standard',
		'Forwarding (IP)',
		'Forwarding (Layer 2)',
		'Reject',
		'Performance (Layer 4)',
		'Performance (HTTP)',
		'Stateless',
	)

class VirtualServerProtocol:
	PROTOCOL_ANY = 0
	PROTOCOL_IPV6 = 1
	PROTOCOL_ROUTING = 2
	PROTOCOL_NONE = 3
	PROTOCOL_FRAGMENT = 4
	PROTOCOL_DSTOPTS = 5
	PROTOCOL_TCP = 6
	PROTOCOL_UDP = 7
	PROTOCOL_ICMP = 8
	PROTOCOL_ICMPV6 = 9
	PROTOCOL_OSPF = 10
	PROTOCOL_SCTP = 11
	
 	PROTOCOLS = (
		'wildcard',
		'IPv6 header',
		'IPv6 routing header',
		'IPv6 no next header',
		'IPv6 fragmentation header',
		'IPv6 destination options',
		'TCP',
		'UDP',
		'ICMP',
		'ICMPv6',
		'OSPF',
		'SCTP',
	)

class LBMethod:
	LB_METHOD_ROUND_ROBIN = 0
	LB_METHOD_RATIO_MEMBER = 1
	LB_METHOD_LEAST_CONNECTION_MEMBER = 2
	LB_METHOD_OBSERVED_MEMBER = 3
	LB_METHOD_PREDICTIVE_MEMBER = 4
	LB_METHOD_RATIO_NODE_ADDRESS = 5
	LB_METHOD_LEAST_CONNECTION_NODE_ADDRESS = 6
	LB_METHOD_FASTEST_NODE_ADDRESS = 7
	LB_METHOD_OBSERVED_NODE_ADDRESS = 8
	LB_METHOD_PREDICTIVE_NODE_ADDRESS = 9
	LB_METHOD_DYNAMIC_RATIO = 10
	LB_METHOD_FASTEST_APP_RESPONSE = 11
	LB_METHOD_LEAST_SESSIONS = 12
	LB_METHOD_DYNAMIC_RATIO_MEMBER = 13
	LB_METHOD_L3_ADDR = 14
	LB_METHOD_UNKNOWN = 15
	LB_METHOD_WEIGHTED_LEAST_CONNECTION_MEMBER = 16
	LB_METHOD_WEIGHTED_LEAST_CONNECTION_NODE_ADDRESS = 17
	LB_METHOD_RATIO_SESSION = 18
	LB_METHOD_RATIO_LEAST_CONNECTION_MEMBER = 19
	LB_METHOD_RATIO_LEAST_CONNECTION_NODE_ADDRESS = 20
	
	LB_METHODS = (
		'Round Robin',
		'Ratio (member)',
		'Least Connections (member)',
		'Observed (member)',
		'Predictive (member)',
		'Ratio (node)',
		'Least Connections (node)',
		'Fastest (node)'
		'Observed (node)',
		'Predictive (node)',
		'Dynamic Ratio (node)',
		'Fastest (application)',
		'Least Sessions',
		'Dynamic Ratio (member)',
		'Layer 3 Address',
		'Unknown',
		'Weighted Least Connections (member)',
		'Weighted Least Connections (node)',
		'Ratio (session)',
		'Ratio Least Connections (member)',
		'Ratio Least Connections (node)',
	)



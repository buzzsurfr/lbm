import os
import bigsuds

from django.utils import timezone
from system.models import Device, DeviceGroup
from ltm.models import Node, Pool, VirtualServer

def connect(device):
	if type(device) != Device:
		#  Throw error and exit
		return None
	
	connection = None
	try:
		connection = bigsuds.BIGIP(device.hostname, device.username, device.password)
		connection = connection.with_session_id()
	except Exception, e:
		pass
	
	return connection

def discover(device_group):
	#  Constants
	status_indicators = {
		'AVAILABILITY_STATUS_GREEN': 'status_circle_green',
		'AVAILABILITY_STATUS_YELLOW': 'status_triangle_yellow',
		'AVAILABILITY_STATUS_RED': 'status_diamond_red',
		'AVAILABILITY_STATUS_BLUE': 'status_square_blue',
		'AVAILABILITY_STATUS_GRAY': 'status_square_gray',
	}
	
	if type(device_group) != DeviceGroup:
		#  Throw error and exit
		return None
	
	#  Connect to active BIG-IP in DeviceGroup
	active_device = device_group.device_set.get(status__contains='active')
	connection = connect(active_device)
	
	#  Get list of virtual servers, pools, and nodes from device
	device_virtual_servers = connection.LocalLB.VirtualServer.get_list()
	device_pools = connection.LocalLB.Pool.get_list()
	
	#  Node
	device_node_list = []
	device_node_addresses = []
	
	device_node_statuses = []
	if active_device.version >= '11.0.0':
		device_node_list = connection.LocalLB.NodeAddressV2.get_list()
		device_node_addresses = connection.LocalLB.NodeAddressV2.get_address(device_node_list)
		device_node_statuses = connection.LocalLB.NodeAddressV2.get_object_status(device_node_list)
	else:
		device_node_list = connection.LocalLB.NodeAddress.get_list()
		device_node_addresses = device_node_list
		device_node_names = connection.LocalLB.NodeAddress.get_screen_name(device_node_addresses)
		#  If name exists (is not empty) replace address in list with name
		for i in range(len(device_node_list)):
			if device_node_names[i]:
				device_node_list[i] = device_node_names[i]
		device_node_statuses = connection.LocalLB.NodeAddress.get_object_status(device_node_addresses)
	
	#  Synchronize device nodes with database list
	
	#  Build Node object list from device data
	device_nodes = [{'name': unicode(os.path.basename(nodename), "utf-8"), 'path': unicode(os.path.dirname(nodename), "utf-8"), 'device_group': device_group} for nodename in device_node_list]
	
	for node in device_nodes:
		try:
			#  Try updating the record
			item = Node.objects.get(node)
			for key, value in node.iteritems():
				setattr(item, key, value)
			item.save()
		except Node.DoesNotExist:
			#  Update failed, create new
			Node.objects.create(**node)
		
	
	#  Build Node object list from device data
#	device_nodes = [Node(name = unicode(os.path.basename(nodename), "utf-8"), path = unicode(os.path.dirname(nodename), "utf-8"), device_group = device_group) for nodename in device_node_list]
	
	#  Add additional data to node instances
#	for i in range(len(device_nodes)):
#		device_nodes[i].address = device_node_addresses[i]
#		device_nodes[i].status_availability, device_nodes[i].status_enabled, device_nodes[i].status_description = device_node_statuses[i]
		#  Compute state for icon based on statuses
#		device_nodes[i].state = status_indicators[device_nodes[i].status_availability]
#		if device_nodes[i].status_enabled == 'ENABLED_STATUS_DISABLED':
#			device_nodes[i].state = device_nodes[i].state.replace('green', 'black').replace('red', 'black')
	
	#  Compare device node to list of db nodes
	

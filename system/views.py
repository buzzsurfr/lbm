import os
import json

import bigsuds

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.utils import timezone

from .models import Device, DeviceGroup
from ltm.models import Node, Pool, PoolMember, VirtualServer

def devicegroup_index(request):
	device_group_list = DeviceGroup.objects.all()
	
	context = {
		'device_group_list': device_group_list,
	}
	
	return render(request, 'system/devicegroup_index.html', context)

def devicegroup_detail(request, devicegroup_id):
	device_group = DeviceGroup.objects.get(pk=devicegroup_id)
	device_count = device_group.device_set.count()
	device_list = device_group.device_set.get_queryset()
	
	context = {
		'device_group': device_group,
		'device_count': device_count,
		'device_list': device_list,
	}
	
	return render(request, 'system/devicegroup_detail.html', context)

def device_index(request):
	device_list = Device.objects.all()
	
	context = {
		'device_list': device_list,
	}
	
	return render(request, 'system/device_index.html', context)

def device_detail(request, device_id):
	device = Device.objects.get(pk=device_id)
	
	context = {
		'device': device,
	}
	
	return render(request, 'system/device_detail.html', context)

def device_test(request, device_id):
	device = Device.objects.get(pk=device_id)
	alerts = []
	
	try:
		conn = bigsuds.BIGIP(device.hostname, device.username, device.password)
		device.status = conn.Management.Device.get_failover_state([device.hostname])[0].lower().replace('ha_state','status_device')
		device.version = conn.System.SystemInfo.get_version()[8:]
		device.updated = timezone.now()
		
		device.save()
		alerts.append({'alert_type': 'success', 'content': "Connection to "+device.name+" successful, "+device.status[14:]+" running "+device.version})
	except Exception, e:
		alerts.append({'alert_type': 'danger', 'content': "Connection to "+device.name+" failed, "+e.message})
	
	context = {
		'device': device,
		'alerts': alerts,
	}
	
	return render(request, 'alerts.html', context)

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
#	device_virtual_servers = connection.LocalLB.VirtualServer.get_list()
	
	#####  Node  #####
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
	
	#  Build Node object list from device data
	device_nodes = [{'name': unicode(os.path.basename(nodename), "utf-8"), 'path': unicode(os.path.dirname(nodename), "utf-8"), 'device_group': device_group} for nodename in device_node_list]
	
	#  Synchronize device nodes with database list
	for i, node in enumerate(device_nodes):
		try:
			#  Try updating the record by getting Node from DB
			item = Node.objects.get(**node)
			
			#  Update node with other attributes before setting to DB
			node['address'] = device_node_addresses[i]
			node['status_availability'] = device_node_statuses[i]['availability_status']
			node['status_enabled'] = device_node_statuses[i]['enabled_status']
			node['status_description'] = device_node_statuses[i]['status_description']
			
			#  Compute state for icon based on statuses
			node['state'] = status_indicators[device_node_statuses[i]['availability_status']]
			if node['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				node['state'] = node['state'].replace('green', 'black').replace('red', 'black')
			
			#  Add Device values to DB object
			for key, value in node.iteritems():
				setattr(item, key, value)
			
			#  Save to DB
			item.save()
			
		except Node.DoesNotExist:
			#  Update failed, create new
			
			#  Update node with other attributes before setting to DB
			node['address'] = device_node_addresses[i]
			node['status_availability'] = device_node_statuses[i]['availability_status']
			node['status_enabled'] = device_node_statuses[i]['enabled_status']
			node['status_description'] = device_node_statuses[i]['status_description']
			
			#  Compute state for icon based on statuses
			node['state'] = status_indicators[device_node_statuses[i]['availability_status']]
			if node['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				node['state'] = node['state'].replace('green', 'black').replace('red', 'black')
			
			item = Node.objects.create(**node)
			
	#####  Pool  #####
	device_pool_list = connection.LocalLB.Pool.get_list()
	device_pool_lb_methods = connection.LocalLB.Pool.get_lb_method(device_pool_list)
	device_pool_statuses = connection.LocalLB.Pool.get_object_status(device_pool_list)
	device_pool_members = []
	if active_device.version >= '11.0.0':
		device_pool_members = connection.LocalLB.Pool.get_member_v2(device_pool_list)
	else:
		device_pool_members = connection.LocalLB.Pool.get_member(device_pool_list)
	device_pool_member_status = connection.LocalLB.Pool.get_member_object_status(device_pool_list, device_pool_members)
	
	#  Build Pool object list from device data
	device_pools = [{'name': unicode(os.path.basename(poolname), "utf-8"), 'path': unicode(os.path.dirname(poolname), "utf-8"), 'device_group': device_group} for poolname in device_pool_list]
	
	#  Synchronize device pools with database list
	for i, pool in enumerate(device_pools):
		try:
			#  Try updating the record by getting Pool from DB
			item = Pool.objects.get(**pool)
			
			#  Update node with other attributes before setting to DB
			pool['lb_method'] = device_pool_lb_methods[i]
			pool['status_availability'] = device_pool_statuses[i]['availability_status']
			pool['status_enabled'] = device_pool_statuses[i]['enabled_status']
			pool['status_description'] = device_pool_statuses[i]['status_description']
			
			#  Compute state for icon based on statuses
			pool['state'] = status_indicators[device_pool_statuses[i]['availability_status']]
			if pool['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				pool['state'] = pool['state'].replace('green', 'black').replace('red', 'black')
			
			#  Add Device values to DB object
			for key, value in pool.iteritems():
				setattr(item, key, value)
			
			#  Save to DB
			item.save()
			
		except Pool.DoesNotExist:
			#  Update failed, create new
			
			#  Update pool with other attributes before setting to DB
			pool['lb_method'] = device_pool_lb_methods[i]
			pool['status_availability'] = device_pool_statuses[i]['availability_status']
			pool['status_enabled'] = device_pool_statuses[i]['enabled_status']
			pool['status_description'] = device_pool_statuses[i]['status_description']
			
			#  Compute state for icon based on statuses
			pool['state'] = status_indicators[device_pool_statuses[i]['availability_status']]
			if pool['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				pool['state'] = pool['state'].replace('green', 'black').replace('red', 'black')
			
			item = Pool.objects.create(**pool)
			
		#  Update members for pool
		for j, member in enumerate(device_pool_members[i]):
			node = Node.objects.get(name=os.path.basename(member['address']), path=os.path.dirname(member['address']), device_group = device_group)
			member_state = status_indicators[device_pool_member_status[i][j]['availability_status']]
			if device_pool_member_status[i][j]['enabled_status'] == 'ENABLED_STATUS_DISABLED':
				member_state = member_state.replace('green', 'black').replace('red', 'black')
			elif device_pool_member_status[i][j]['enabled_status'] == 'ENABLED_STATUS_DISABLED_BY_PARENT':
				member_state = member_state.replace('green', 'gray').replace('red', 'gray')
			
			try:
				poolmember = item.poolmember_set.get(node__name=unicode(os.path.basename(member['address']), "utf-8"), node__path=unicode(os.path.dirname(member['address']), "utf-8"), port=member['port'])
				setattr(poolmember, 'state', member_state)
				poolmember.save()
			except PoolMember.DoesNotExist:
				PoolMember.objects.create(pool=item, node=node, port=member['port'], state=member_state)
	
	#####  VirtualServer  #####
	device_vs_list = connection.LocalLB.VirtualServer.get_list()
	device_vs_descriptions = connection.LocalLB.VirtualServer.get_description(device_vs_list)
	device_vs_types = connection.LocalLB.VirtualServer.get_type(device_vs_list)
	if active_device.version >= '11.0.0':
		device_vs_destinations = connection.LocalLB.VirtualServer.get_destination_v2(device_vs_list)
	else:
		device_vs_destinations = connection.LocalLB.VirtualServer.get_destination(device_vs_list)
	device_vs_subnets = connection.LocalLB.VirtualServer.get_wildmask(device_vs_list)	
	device_vs_statuses = connection.LocalLB.VirtualServer.get_object_status(device_vs_list)
	device_vs_protocols = connection.LocalLB.VirtualServer.get_protocol(device_vs_list)
	device_vs_pools = connection.LocalLB.VirtualServer.get_default_pool_name(device_vs_list)
	
	#  Build Node object list from device data
	device_virtualservers = [{'name': unicode(os.path.basename(vs_name), "utf-8"), 'path': unicode(os.path.dirname(vs_name), "utf-8"), 'device_group': device_group} for vs_name in device_vs_list]
	
	#  Synchronize device nodes with database list
	for i, virtualserver in enumerate(device_virtualservers):
		try:
			#  Try updating the record by getting Node from DB
			item = VirtualServer.objects.get(**virtualserver)
			
			#  Update node with other attributes before setting to DB
			virtualserver['description'] = device_vs_descriptions[i]
			virtualserver['vs_type'] = device_vs_types[i]
			virtualserver['destination'] = os.path.basename(device_vs_destinations[i]['address'])
			virtualserver['destination_subnet'] = device_vs_subnets[i]
			virtualserver['service_port'] = device_vs_destinations[i]['port']
			virtualserver['status_availability'] = device_vs_statuses[i]['availability_status']
			virtualserver['status_enabled'] = device_vs_statuses[i]['enabled_status']
			virtualserver['status_description'] = device_vs_statuses[i]['status_description']
			if device_vs_pools[i]:
				virtualserver['pool'] = Pool.objects.get(name=os.path.basename(device_vs_pools[i]), path=os.path.dirname(device_vs_pools[i]), device_group = device_group)
			
			#  Compute state for icon based on statuses
			virtualserver['state'] = status_indicators[device_vs_statuses[i]['availability_status']]
			if virtualserver['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				virtualserver['state'] = virtualserver['state'].replace('green', 'black').replace('red', 'black')
			elif virtualserver['status_enabled'] == 'ENABLED_STATUS_DISABLED_BY_PARENT':
				virtualserver['state'] = virtualserver['state'].replace('green', 'gray').replace('red', 'gray')
			
			#  Add Device values to DB object
			for key, value in virtualserver.iteritems():
				setattr(item, key, value)
			
			#  Save to DB
			item.save()
			
		except VirtualServer.DoesNotExist:
			#  Update failed, create new
			
			#  Update node with other attributes before setting to DB
			virtualserver['description'] = device_vs_descriptions[i]
			virtualserver['vs_type'] = device_vs_types[i]
			virtualserver['destination'] = device_vs_destinations[i]['address']
			virtualserver['destination_subnet'] = device_vs_subnets[i]
			virtualserver['service_port'] = device_vs_destinations[i]['port']
			virtualserver['status_availability'] = device_vs_statuses[i]['availability_status']
			virtualserver['status_enabled'] = device_vs_statuses[i]['enabled_status']
			virtualserver['status_description'] = device_vs_statuses[i]['status_description']
			if device_vs_pools[i]:
				virtualserver['pool'] = Pool.objects.get(name=os.path.basename(device_vs_pools[i]), path=os.path.dirname(device_vs_pools[i]), device_group = device_group)
			
			#  Compute state for icon based on statuses
			virtualserver['state'] = status_indicators[device_vs_statuses[i]['availability_status']]
			if virtualserver['status_enabled'] == 'ENABLED_STATUS_DISABLED':
				virtualserver['state'] = virtualserver['state'].replace('green', 'black').replace('red', 'black')
			elif virtualserver['status_enabled'] == 'ENABLED_STATUS_DISABLED_BY_PARENT':
				virtualserver['state'] = virtualserver['state'].replace('green', 'gray').replace('red', 'gray')
			
			item = VirtualServer.objects.create(**virtualserver)
			
def devicegroup_generate_inventory(request):
	inventory_type = request.GET.get('format') or 'dump'
	
	if inventory_type == 'dump':
		devicegroup_inventory = json.loads(serializers.serialize('json', DeviceGroup.objects.all()))
		device_inventory = json.loads(serializers.serialize('json', Device.objects.all()))
		response = JsonResponse(devicegroup_inventory + device_inventory, safe=False)
		response['Content-Disposition'] = 'attachment; filename="lbm.json"'
		return response
	elif inventory_type == 'ansible':
		export = ''
		for device_group in DeviceGroup.objects.all():
			export += '[' + device_group.name + ']\n'
			for device in device_group.device_set.values():
				export += device['name']
				for prop in ('hostname', 'username', 'password'):
					export += ' ' + prop + '=' + device[prop]
				export += '\n'
			export += '\n'
		response = HttpResponse(export, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename="lbm.hosts"'
		return response
	else:
		return None

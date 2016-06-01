from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

import ltm.structs
from .models import *

def node_index(request):
	node_list = Node.objects.all()
	paginator = Paginator(node_list, 25)

	page = request.GET.get('page')

	try:
		nodes = paginator.page(page)
	except PageNotAnInteger:
		nodes = paginator.page(1)
	except EmptyPage:
		nodes = paginator.page(paginator.num_pages)

	context = {
		'node_list': node_list,
		'nodes': nodes,
	}

	return render(request, 'ltm/node_index.html', context)

def node_detail(request, node_id):
	node = Node.objects.get(pk=node_id)
	active_device = node.device_group.device_set.get(status__contains='active')

	context = {
		'node': node,
		'active_device': active_device,
	}

	return render(request, 'ltm/node_detail.html', context)

def pool_index(request):
	pool_list = [{'id': pool.id, 'name': pool.name, 'method': ltm.structs.lb_method[pool.lb_method]['name'], 'state': pool.state, 'monitor_count': 0, 'member_count': pool.poolmember_set.count(), 'device_group': pool.device_group.name} for pool in Pool.objects.all()]
	paginator = Paginator(pool_list, 25)

	page = request.GET.get('page')

	try:
		pools = paginator.page(page)
	except PageNotAnInteger:
		pools = paginator.page(1)
	except EmptyPage:
		pools = paginator.page(paginator.num_pages)

	context = {
		'pool_list': pool_list,
		'pools': pools,
	}

	return render(request, 'ltm/pool_index.html', context)

def pool_detail(request, pool_id):
	pool = Pool.objects.get(pk=pool_id)
	pool_lb_method = ltm.structs.lb_method[pool.lb_method]['name']
	pool_lb_method_description = ltm.structs.lb_method[pool.lb_method]['description']
	active_device = pool.device_group.device_set.get(status__contains='active')
	member_count = pool.poolmember_set.count()
	members = pool.poolmember_set.all()

	context = {
		'pool': pool,
		'pool_lb_method': pool_lb_method,
		'pool_lb_method_description': pool_lb_method_description,
		'active_device': active_device,
		'member_count': member_count,
		'members': members,
	}

	return render(request, 'ltm/pool_detail.html', context)

def virtualserver_index(request):
	virtual_server_list = VirtualServer.objects.all()

	paginator = Paginator(virtual_server_list, 25)

	page = request.GET.get('page')

	try:
		virtual_servers = paginator.page(page)
	except PageNotAnInteger:
		virtual_servers = paginator.page(1)
	except EmptyPage:
		virtual_servers = paginator.page(paginator.num_pages)

	context = {
#		'virtual_server_list': virtual_server_list,
		'virtual_servers': virtual_servers,
	}

	return render(request, 'ltm/virtualserver_index.html', context)

def virtualserver_detail(request, virtualserver_id):
	virtual_server = VirtualServer.objects.get(pk=virtualserver_id)
	pool_meta = {
		'lb_method_name': ltm.structs.lb_method[virtual_server.pool.lb_method]['name'],
		'lb_method_description': ltm.structs.lb_method[virtual_server.pool.lb_method]['description'],
	}
	active_device = virtual_server.device_group.device_set.get(status__contains='active')
	member_count = virtual_server.pool.poolmember_set.count()
	pool_members = virtual_server.pool.poolmember_set.all()

	context = {
		'virtual_server': virtual_server,
		'active_device': active_device,
		'pool': virtual_server.pool,
		'pool_meta': pool_meta,
		'member_count': member_count,
		'members': pool_members,
	}

	return render(request, 'ltm/virtualserver_detail.html', context)

def index(request):
	#  VirtualServer stats
	virtual_server_list = VirtualServer.objects.all()
	virtual_server_stat_list = virtual_server_list.values('status_availability').annotate(count=Count('status_availability'))
	virtual_server_stats = {key: 0 for key in ltm.structs.availability_status.keys()}
	virtual_server_stats['total'] = 0
	for stat in virtual_server_stat_list:
		virtual_server_stats[stat['status_availability']] = stat['count']
		virtual_server_stats['total'] += stat['count']

	#  Pool stats
	pool_list = Pool.objects.all()
	pool_stat_list = pool_list.values('status_availability').annotate(count=Count('status_availability'))
	pool_stats = {key: 0 for key in ltm.structs.availability_status.keys()}
	pool_stats['total'] = 0
	for stat in pool_stat_list:
		pool_stats[stat['status_availability']] = stat['count']
		pool_stats['total'] += stat['count']

	#  Node stats
	node_list = Node.objects.all()
	node_stat_list = node_list.values('status_availability').annotate(count=Count('status_availability'))
	node_stats = {key: 0 for key in ltm.structs.availability_status.keys()}
	node_stats['total'] = 0
	for stat in node_stat_list:
		node_stats[stat['status_availability']] = stat['count']
		node_stats['total'] += stat['count']

	context = {
		'virtual_server_stats': virtual_server_stats,
#		'virtual_server_list': virtual_server_list,
		'pool_stats': pool_stats,
#		'pool_list': pool_list,
		'node_stats': node_stats,
#		'node_list': node_list,
	}

	return render(request, 'ltm/index.html', context)

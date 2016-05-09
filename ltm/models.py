from __future__ import unicode_literals

import netaddr

from django.db import models

from system.models import DeviceGroup
from .structures import *

class Node(models.Model):
	name = models.CharField(max_length=255)
	path = models.CharField(max_length=255, default='/Common')
	address = models.GenericIPAddressField()
	state = models.CharField(max_length=200)
	status_availability = models.CharField(max_length=64)
	status_enabled = models.CharField(max_length=64)
	status_description = models.CharField(max_length=255)
#	monitors (many-to-many)
	
	#  Resources
	device_group = models.ForeignKey(DeviceGroup, on_delete=models.CASCADE, blank=True, null=True) #remove blank and null after adjusting data
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name and self.path == other.path and self.device_group == other.device_group
	
	def __ne__(self, other):
		return not isinstance(other, self.__class__) or self.name != other.name or self.path != other.path or self.device_group != other.device_group

class Pool(models.Model):
	#  Properties
	name = models.CharField(max_length=255)
	path = models.CharField(max_length=255, default='/Common')
	state = models.CharField(max_length=200)
	status_availability = models.CharField(max_length=64)
	status_enabled = models.CharField(max_length=64)
	status_description = models.CharField(max_length=255)
	
	#  Methods
	lb_method = models.CharField(max_length=255)
	members = models.ManyToManyField(Node, through='PoolMember')
	
	#  Resources
	device_group = models.ForeignKey(DeviceGroup, on_delete=models.CASCADE, blank=True, null=True) #remove blank and null after adjusting data
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name and self.path == other.path and self.device_group == other.device_group
	
	def __ne__(self, other):
		return not isinstance(other, self.__class__) or self.name != other.name or self.path != other.path or self.device_group != other.device_group

class PoolMember(models.Model):
	#  Properties
	port = models.IntegerField()
	state = models.CharField(max_length=64)
#	monitors
	
	#  Configuration
#	ratio = models.IntegerField()
#	priority_group = models.IntegerField()
#	connection_limit = models.IntegerField()
	
	#  Relationship
	pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
	node = models.ForeignKey(Node, on_delete=models.CASCADE)
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.node.name + ':' + unicode(str(self.port), "utf-8")

class VirtualServerProfile(models.Model):
	name = models.CharField(max_length=255)
	
	def __str__(self):
		return self.name

class VirtualServer(models.Model):
	#  Properties
	name = models.CharField(max_length=255)
	path = models.CharField(max_length=255, default='/Common')
	description = models.CharField(max_length=255)
	vs_type = models.CharField(max_length=64)
#	source = models.CharField(max_length=64)
	destination = models.GenericIPAddressField()
	destination_subnet = models.GenericIPAddressField()
	service_port = models.IntegerField()
	state = models.CharField(max_length=200)
	status_availability = models.CharField(max_length=64)
	status_enabled = models.CharField(max_length=64)
	status_description = models.CharField(max_length=255)
	protocol = models.IntegerField(choices=enumerate(VirtualServerProtocol.PROTOCOLS), default=VirtualServerProtocol.PROTOCOL_TCP)
	
	#  Resources
	pool = models.ForeignKey(Pool, on_delete=models.CASCADE, blank=True, null=True)
	device_group = models.ForeignKey(DeviceGroup, on_delete=models.CASCADE, blank=True, null=True) #remove blank and null after adjusting data
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name and self.path == other.path and self.device_group == other.device_group
	
	def __ne__(self, other):
		return not isinstance(other, self.__class__) or self.name != other.name or self.path != other.path or self.device_group != other.device_group



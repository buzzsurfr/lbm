from __future__ import unicode_literals

from django.db import models

class DeviceGroup(models.Model):
	F5_BIGIP = 'F5 BIG-IP'
	DEVICE_TYPES = (
		(F5_BIGIP, 'F5 BIG-IP'),
	)
	
	name = models.CharField(max_length=200)
	classification = models.CharField(
		max_length=200,
		choices = DEVICE_TYPES,
		default = F5_BIGIP
	)
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name

class Device(models.Model):
	F5_BIGIP = 'F5 BIG-IP'
	DEVICE_TYPES = (
		(F5_BIGIP, 'F5 BIG-IP'),
	)
	
	name = models.CharField(max_length=200)
	classification = models.CharField(
		max_length=200,
		choices = DEVICE_TYPES,
		default = F5_BIGIP
	)
	version = models.CharField(max_length=32)
	connection = models.CharField(
		max_length=200,
		default = 'bigsuds'
	)
	status = models.CharField(max_length=64, null=True)
	device_group = models.ForeignKey(DeviceGroup, on_delete=models.PROTECT)
	
	# Connection
	hostname = models.CharField(max_length=200)
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	
	# Meta
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


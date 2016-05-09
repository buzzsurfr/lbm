from django.test import TestCase

from .models import Device, DeviceGroup

# Create your tests here.
class DeviceTestCase(TestCase):
	
	def setUp(self):
		DeviceGroup.objects.create(name='device_group_1', classification='F5 BIG-IP')
		DeviceGroup.objects.create(name='device_group_2', classification='F5 BIG-IP')
		
		Device.objects.create(name='device_1', classification='F5 BIG-IP', hostname='device_1', connection='bigsuds', username='admin', password='admin', device_group=DeviceGroup.objects.get(pk=1))
		Device.objects.create(name='device_2', classification='F5 BIG-IP', hostname='device_1', connection='bigsuds', username='admin', password='admin', device_group=DeviceGroup.objects.get(pk=2))
	
	def test_all_fields_assigned(self):
		device_1 = Device.objects.get(name='device_1')
		self.assertEqual(device_1.pk, 1)


from django.conf.urls import url

from . import views

app_name = 'system'
urlpatterns = [
	url(r'^device_group/$', views.devicegroup_index, name='device_group_index'),
	url(r'^device_group/(?P<devicegroup_id>[0-9]+)/$', views.devicegroup_detail, name='device_group_detail'),
	url(r'^device/$', views.device_index, name='device_index'),
	url(r'^device/(?P<device_id>[0-9]+)/$', views.device_detail, name='device_detail'),
	url(r'^device/(?P<device_id>[0-9]+)/test/$', views.device_test, name='device_test'),
	url(r'^export/$', views.devicegroup_generate_inventory, name='devicegroup_generate_inventory'),
]

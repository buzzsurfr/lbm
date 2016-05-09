from django.conf.urls import url

from . import views

app_name = 'ltm'
urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^node/$', views.NodeIndexView.as_view(), name='node_index'),
	url(r'^node/$', views.node_index, name='node_index'),
#	url(r'^node/(?P<pk>[0-9]+)/$', views.NodeDetailView.as_view(), name='node_detail'),
	url(r'^node/(?P<node_id>[0-9]+)/$', views.node_detail, name='node_detail'),
#	url(r'^pool/$', views.PoolIndexView.as_view(), name='pool_index'),
	url(r'^pool/$', views.pool_index, name='pool_index'),
	url(r'^pool/(?P<pool_id>[0-9]+)/$', views.pool_detail, name='pool_detail'),
#	url(r'^virtual_server/$', views.VirtualServerIndexView.as_view(), name='virtual_server_index'),
	url(r'^virtual_server/$', views.virtualserver_index, name='virtual_server_index'),
#	url(r'^virtual_server/(?P<pk>[0-9]+)/$', views.VirtualServerDetailView.as_view(), name='virtual_server_detail'),
	url(r'^virtual_server/(?P<virtualserver_id>[0-9]+)/$', views.virtualserver_detail, name='virtual_server_detail'),
]

from django.contrib import admin

from .models import *

class PoolMemberInline(admin.TabularInline):
	model = PoolMember
	fields = ('state', 'node', 'port',)
	extra = 1

class NodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('General Properties', {'fields': [
			'address',
			'name',
			'path',
			'state',
			'status_availability',
			'status_enabled',
			'status_description',
			'device_group',
		]}),
#		('Configuration', {'fields': [		]}),
	]
	list_display = ('name', 'address')

class PoolAdmin(admin.ModelAdmin):
	fieldsets = [
		('General Properties', {'fields': [
			'name',
			'path',	
			'state',
			'device_group',
		]}),
		('Load Balancing', {'fields': [
			'lb_method',
		]}),
	]
	list_display = ('name', 'member_count')
	inlines = (PoolMemberInline,)
	
	def member_count(self, pool):
		return pool.poolmember_set.count()

admin.site.register(VirtualServer)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Node, NodeAdmin)

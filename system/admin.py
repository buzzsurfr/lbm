from django.contrib import admin

from .models import DeviceGroup, Device

class DeviceInline(admin.TabularInline):
	model = Device
	fields = ('status', 'name', 'classification', 'version', 'connection')
	readonly_fields = ('status', 'name', 'classification', 'version', 'connection')
	can_delete = False
	show_change_link = True
	extra = 0
	editable_fields = []
	
	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request):
		return False

class DeviceGroupAdmin(admin.ModelAdmin):
	fieldsets = [
		('General Properties', {'fields': [
			'name',
		]}),
	]
	list_display = ('name', 'device_count')
	inlines = (DeviceInline,)
	
	def device_count(self, device_group):
		return device_group.device_set.count()






# Register your models here.
admin.site.register(DeviceGroup, DeviceGroupAdmin)
admin.site.register(Device)

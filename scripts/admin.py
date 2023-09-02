
from django.contrib import admin
from .models import NetworkDeviceInfo, NetworkDeviceLog

@admin.register(NetworkDeviceInfo)
class NetworkDeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'host_name', 'info')

@admin.register(NetworkDeviceLog)
class NetworkDeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'created_at')

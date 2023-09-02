
from django.contrib import admin
from .models import NetworkDeviceInfo

@admin.register(NetworkDeviceInfo)
class NetworkDeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'host_name', 'info')



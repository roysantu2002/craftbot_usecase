from rest_framework import serializers
from .models import NetworkDeviceInfo

class NetworkDeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDeviceInfo
        fields = ('id', 'ip_address', 'host_name', 'info')


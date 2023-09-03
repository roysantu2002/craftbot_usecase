from rest_framework import serializers
from .models import NetworkDeviceInfo, NetworkDeviceLog

class ExecuteScriptSerializer(serializers.Serializer):
    script_room = serializers.CharField()

class NetworkDeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDeviceInfo
        fields = ('id', 'ip_address', 'host_name', 'info')

class NetworkDeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDeviceLog
        fields = '__all__'
